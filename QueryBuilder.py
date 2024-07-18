class QueryBuilder:

    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name
        self.conditions = []
        self.joins = []
        self.lookup_field_conditions = [
            "gt", "gte", "lt", "lte", "ne", "in", "nin", "like", "nlike", "is"]
        self.limit_value = None
        self.offset_value = None
        self.orderby_fields = None
        self.orderby_desc = False
        self.groupby_fields = None

    def all(self, verbose=False, isDict=False):
        if self.groupby_fields is None:
            query = self._execute_query(f"SELECT * FROM {self.table_name} ")
        else:
            query = self._execute_query(
                f"SELECT {self.groupby_fields} FROM {self.table_name} ")
        if verbose:
            print(query + "\n")
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        if isDict:
            result = [dict(zip(columns, row)) for row in results]
        result = columns, results
        cursor.close()
        if verbose:
            print(result, "\n")

    def values(self, values, verbose=False, isDict=False):
        query = self._execute_query(f"SELECT {values} FROM {self.table_name} ")
        if verbose:
            print(query + "\n")
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        if isDict:
            result = [dict(zip(columns, row)) for row in results]
        result = columns, results
        cursor.close()
        if verbose:
            print(result, "\n")

    def limit(self, limit_value, offset_value=None):
        self.limit_value = limit_value
        if offset_value is not None:
            self.offset_value = offset_value
        return self

    def orderby(self, fields, descending=False):
        self.orderby_fields = fields
        self.orderby_descending = descending
        return self

    def groupby(self, fields):
        self.groupby_fields = fields
        return self

    def _handle_lookup(self, key, value):
        lookup_list = key.split("__")
        lookup_list.insert(0, self.table_name)
        lookup_condition = ""
        lookup_table_field = ""

        if lookup_list[-1] in self.lookup_field_conditions:
            lookup_condition = lookup_list.pop()
            lookup_table_field = lookup_list.pop()
        else:
            lookup_table_field = lookup_list.pop()

        # Create joins
        if len(lookup_list) > 1:
            self._create_join(lookup_list)

        # Create conditions
        join_condition_query = ""

        if lookup_condition == "is":
            field_value = ""
            if type(value).__name__ == "NoneType":
                field_value = "NULL"
            else:
                field_value = f"'{value}'" if type(
                    value).__name__ == "str" else value
            join_condition_query = f"{lookup_list[-1]}.{lookup_table_field} IS {field_value}"
            self.conditions.append(join_condition_query)

        elif lookup_condition == "in" or lookup_condition == "nin":
            field_value_list = value
            new_field_value_list = [str(fvalue) if not isinstance(
                fvalue, str) else f"'{fvalue}'" for fvalue in field_value_list]
            values_tuple = ", ".join(new_field_value_list)
            if lookup_condition == "in":
                join_condition_query = f"{lookup_list[-1]}.{lookup_table_field} IN ({values_tuple})"
            elif lookup_condition == "nin":
                join_condition_query = f"{lookup_list[-1]}.{lookup_table_field} NOT IN ({values_tuple})"
            self.conditions.append(join_condition_query)

        else:
            if lookup_condition == "gt":
                lookup_condition = ">"
            elif lookup_condition == "gte":
                lookup_condition = ">="
            elif lookup_condition == "lt":
                lookup_condition = "<"
            elif lookup_condition == "lte":
                lookup_condition = "<="
            elif lookup_condition == "ne":
                lookup_condition = "<>"
            elif lookup_condition == "":
                lookup_condition = "="
            elif lookup_condition == "like":
                lookup_condition = "LIKE"
            elif lookup_condition == "nlike":
                lookup_condition = "NOT LIKE"
            field_value = f"'{value}'" if type(
                value).__name__ == "str" else value
            join_condition_query = f"{lookup_list[-1]}.{lookup_table_field} {lookup_condition} {field_value}"
            self.conditions.append(join_condition_query)

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            self._handle_lookup(key, value)
        return self

    def _create_join(self, lookup_list):
        for i in range(1, len(lookup_list)):
            join_query = f"\nINNER JOIN {lookup_list[i]} ON {lookup_list[i-1]}.{lookup_list[i]}_id = {lookup_list[i]}.id"
            if not join_query in self.joins:
                self.joins.append(join_query)
        return self

    def _execute_query(self, query):
        if len(self.joins) > 0:
            joins_str = " ".join(self.joins)
            query += joins_str
        if len(self.conditions) > 0:
            conditions_str = " AND ".join(self.conditions)
            query += f"\nWHERE {conditions_str}"
        if self.groupby_fields is not None:
            query += f"\nGROUP BY {self.groupby_fields}"
        if self.orderby_fields is not None:
            query += f"\nORDER BY {self.orderby_fields}"
            if self.orderby_descending == True:
                query += " DESC "
            else:
                query += " ASC "
        if self.limit_value is not None:
            query += f"\nLIMIT {self.limit_value} "
            if self.offset_value is not None:
                query += f" OFFSET {self.offset_value} "
        query += ";"
        return query
