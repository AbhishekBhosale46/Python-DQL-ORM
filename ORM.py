import psycopg2
from . import QueryBuilder


class ORM:

    def __init__(self, db_name, db_user, db_password, db_host, db_port):

        self.connection = psycopg2.connect(dbname=db_name,
                                           user=db_user,
                                           password=db_password,
                                           host=db_host,
                                           port=db_port)

    def __getattr__(self, table_name):
        return QueryBuilder(self.connection, table_name)

    def raw(self, query, verbose=False, isDict=False):
        if verbose:
            print(query + "\n")
        cursor = self.connection.cursor()
        cursor.execute(query)
        cr = cursor.fetchall()
        cd = [x[0] for x in cursor.description]
        if isDict:
            result = [dict(zip(cd, row)) for row in cr]
        result = cd, cr
        cursor.close()
        if verbose:
            print(result, "\n")
