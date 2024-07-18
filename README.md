# 🛢️⚒️ Python DQL ORM

A lightweight Python ORM focused on DQL (Data Query Language) operations, providing an easy-to-use interface for building and executing SQL queries. This ORM supports advanced querying features such as filtering, joins, ordering, grouping, and more.

## Features

**Simple and Intuitive API**: Build and execute SQL queries using a Pythonic interface.
**Advanced Filtering**: Support for a variety of lookup conditions (gt, gte, lt, lte, ne, in, nin, like, nlike, is).
**Joins**: Easily perform joins between tables.
**Ordering and Grouping**: Order and group query results.
**Limit and Offset**: Support for pagination.

## Usage

To install the ORM, clone this repository and install the required dependencies

```
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

# RAW SQL QUERIES
orm.raw("SELECT * FROM data ;")
orm.raw("SELECT * FROM data ;")

```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.
