from . import ORM

orm = ORM(db_name="DB_NAME", 
          db_user="DB_USER",
          db_password="DB_PASS", 
          db_host="DB_HOST", 
          db_port="DB_PORT")


# GET ALL RECORDS
orm.Student.all()

# FILTER RECORDS
orm.Student.filter(name="Abhishek", age=18, college="PICT").all()

# FILTER CHAINING
orm.Student.filter(name="Abhishek", age=18).filter(college="PICT").all()

# FILTER ALONG WITH JOIN
orm.Student.filter(college__name='PICT').all()

# FILTER ALONG WITH MULTIPLE JOINS
orm.Student.filter(college__name='PICT', city__name='Kolhapur').all()

# FILTER ALONG WITH MULTIPLE JOINS AND CONDITIONS
orm.Student.filter(college__name='PICT', city__name='Kolhapur', age=18).all()

# FILTER ALONG WITH MULTIPLE TABLE JOINS
orm.Review.filter(book__author__table3__name="Abhishek").all()

# GET SPECIFIC VALUES
orm.Student.filter(name="Abhishek", age=18, college="PICT").values("name, age, city")
orm.Student.filter(college__name='PICT', city__name='Kolhapur', age=18).values("name, age, city")

# FILTER ALONG WITH CONDITIONS
orm.Student.filter(age__ne=18).all()
orm.Student.filter(age__gte=18).all()
orm.Student.filter(college__city__street__name="ABC").all()
orm.Student.filter(college__city__table3__table4__table5__name__lte="ABC",college__city__table5__o=1).values('city.name,table5.name')
orm.Student.filter(college__name__ne='PICT', city__name='Kolhapur', age__lt=18).all()
orm.Member.filter(table1__table2__table3__firstname__in=['Tobias', 'Linus', 'John', 1, 2, 3]).all()
orm.Student.filter(name__like="_bhi").all()
orm.Student.filter(city__name__like="a%").all()
orm.Student.filter(city__name__is="a%").all()
orm.Student.filter(city__name__is=None).all()

# RAW SQL QUERIES
orm.raw("SELECT * FROM tbl_master ;")
orm.raw("SELECT * FROM tbl_master ;")