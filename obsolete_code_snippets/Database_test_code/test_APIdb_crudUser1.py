# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# test_APIdb_crudUser1.py

# Testing CRUD for User -model of Image Annotator

"""
In order to run this test code of ImageAnnotator flask API.

Add following files and folders to ImageAnnotator -folder:
* ImageTest -folder including test images from web
* Phototest -folder including test private photos
* imageAnnoAPI.py -file
* test_APIdb_crudUser1.py

ImageAnnotator -folder includes also
* .venv -folder (python virtual environment)
* .vscode -folder (VSC launch and settings)

Activate created python virtual environment (on VSC cmd):
    cd C:\PWBproject\ImageAnnotator\.venv\Scripts
    activate.bat

Go to ImageAnnotator folder:
    (.venv) C:\PWBproject\ImageAnnotator>

Run test file by command:
    python test_APIdb_crudUser1.py

TESTING
* CRUD -functions
* create - create_all() and add functions
* read - SQL query functions
* update - update function 
* delete - delete and drop_all()

RESULTS
* available at the end of the code

"""

from imageAnnoAPI import db
from imageAnnoAPI import ImageContent, PhotoContent, ImageAnnotation, PhotoAnnotation, User

from datetime import datetime
import glob
import base64
from io import BytesIO
import os

# -------------------------------------------------------------------
# Create database including all defined models

db.create_all()

print("\n Database created succesfully ")

# -------------------------------------------------------------------
# Testing User -model with CRUD -functions

# Create new row for new user to database by using User -model
user1 = User(user_name = "Meria Developer")
user2 = User(user_name = "Juha Engineer")
user3 = User(user_name = "Matti Meikäläinen")

# Add model to to the session
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Save session to database with commit
db.session.commit()

print("\n ADD USER ")

# Execute SQL query for database by using Model.query
# OR for db.session.query(Model)
# query.all() get all rows in the database as a list
result_users = User.query.all()
for item in result_users:
    print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)

# -------------------------------------------------------------------
# Add new users to existing User -model
user4 = User(user_name = "Katti ole' Matikainen")
user5 = User(user_name = "Hessu Hopo :-) ")
user6 = User(user_name = "Matti Meikäläinen")
user7 = User(user_name = "Juha Engineer")

db.session.add_all([user4, user5, user6, user7])
# Save session to database with commit
db.session.commit()

print("\n ADD NEW USER ")

# Execute SQL query for database by using Model.query
# OR for db.session.query(Model)
# query.all() get all rows in the database as a list
result_users = User.query.all()
for item in result_users:
    print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)

# ----------------------------------------------------------------------
# Delete the first user with defined username

define_user = User.query.filter_by(user_name = "Matti Meikäläinen").first()
db.session.delete(define_user)
db.session.commit()

print("\n DELETE Matti FROM USER ")

result_users = User.query.all()
for item in result_users:
    print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)

# ----------------------------------------------------------------------
# Delete all users with defined username

# CANNOT execute delete for all defined user names simultaneously
"""
define_user = User.query.filter_by(user_name = "Juha Engineer").all()
db.session.delete(define_user)
db.session.commit()

print("\n DELETE all Juha Engineer FROM USER ")

result_users = User.query.all()
for item in result_users:
    print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)
"""

# ----------------------------------------------------------------------
# Update the values of existing User -model (change item data)

User.query.filter_by(id=4).update({'user_name': 'Katti von Matikainen'})

# The updated model have already been added to the session
db.session.commit()

print("\n UPDATE user id 4 AT USER TO Katti von Matikainen ")

result_users = User.query.all()
for item in result_users:
    print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)

# -----------------------------------------------------------------------
# QUERY - asending and desending order

# By default, SQLAlchemy returns the records ordered by their primary keys. 
# To return by user_name asending or desending order use order_by -function

print("\n Asending order for user_name ")

# asending
result_users = User.query.order_by(User.user_name).all()
for item in result_users:
    print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)

print("\n Desending order for user_name ")

# desending
result_users = User.query.order_by(User.user_name.desc()).all()
for item in result_users:
    print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)

# --------------------------------------------------------------------------
# Add new users with user id and user_name

user8 = User(id=11, user_name = "Anni McLennox")
user9 = User(id=20, user_name = ";-(( sad cat *//*")

db.session.add_all([user8, user9])
# Save session to database with commit
db.session.commit()

print("\n ADD NEW USER WITH id and user_name ")

# Execute SQL query for database by using Model.query
# OR for db.session.query(Model)
# query.all() get all rows in the database as a list
result_users = User.query.all()
for item in result_users:
    print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)

# -------------------------------------------------------------------------
# Return defined model item (row) by its primary key
# use query.get() -function

print("\n RETURN item (row) WITH PRIMARY KEY ")

item = User.query.get(5)
print("\nUser object:", item ,"   User ID: ", item.id, "   Username", item.user_name)

# -------------------------------------------------------------------
# Remove all the data in database with drop_all()

print("\n  REMOVE ALL DATABASE \n")

db.drop_all()

# check results with User -model
result_users = User.query.all()
for item in result_users:
    print("\n User in database: " + item.user_name)

# -------------------------------------------------------------------

"""
RESULTS  ---------------------------------------------------------------

Database created succesfully 

 ADD USER 

User object: <User 1>    User ID:  1    Username Meria Developer  

User object: <User 2>    User ID:  2    Username Juha Engineer    

User object: <User 3>    User ID:  3    Username Matti Meikäläinen

 ADD NEW USER 

User object: <User 1>    User ID:  1    Username Meria Developer  

User object: <User 2>    User ID:  2    Username Juha Engineer    

User object: <User 3>    User ID:  3    Username Matti Meikäläinen

User object: <User 4>    User ID:  4    Username Katti ole' Matikainen

User object: <User 5>    User ID:  5    Username Hessu Hopo :-)

User object: <User 6>    User ID:  6    Username Matti Meikäläinen

User object: <User 7>    User ID:  7    Username Juha Engineer

 DELETE Matti FROM USER

User object: <User 1>    User ID:  1    Username Meria Developer

User object: <User 2>    User ID:  2    Username Juha Engineer

User object: <User 4>    User ID:  4    Username Katti ole' Matikainen

User object: <User 5>    User ID:  5    Username Hessu Hopo :-)

User object: <User 6>    User ID:  6    Username Matti Meikäläinen

User object: <User 7>    User ID:  7    Username Juha Engineer

 UPDATE user id 4 AT USER TO Katti von Matikainen

User object: <User 1>    User ID:  1    Username Meria Developer

User object: <User 2>    User ID:  2    Username Juha Engineer

User object: <User 4>    User ID:  4    Username Katti von Matikainen

User object: <User 5>    User ID:  5    Username Hessu Hopo :-)

User object: <User 6>    User ID:  6    Username Matti Meikäläinen

User object: <User 7>    User ID:  7    Username Juha Engineer

 Asending order for user_name

User object: <User 5>    User ID:  5    Username Hessu Hopo :-)

User object: <User 2>    User ID:  2    Username Juha Engineer

User object: <User 7>    User ID:  7    Username Juha Engineer

User object: <User 4>    User ID:  4    Username Katti von Matikainen

User object: <User 6>    User ID:  6    Username Matti Meikäläinen

User object: <User 1>    User ID:  1    Username Meria Developer

 Desending order for user_name

User object: <User 1>    User ID:  1    Username Meria Developer

User object: <User 6>    User ID:  6    Username Matti Meikäläinen

User object: <User 4>    User ID:  4    Username Katti von Matikainen

User object: <User 2>    User ID:  2    Username Juha Engineer

User object: <User 7>    User ID:  7    Username Juha Engineer

User object: <User 5>    User ID:  5    Username Hessu Hopo :-)

 ADD NEW USER WITH id and user_name

User object: <User 1>    User ID:  1    Username Meria Developer

User object: <User 2>    User ID:  2    Username Juha Engineer

User object: <User 4>    User ID:  4    Username Katti von Matikainen

User object: <User 5>    User ID:  5    Username Hessu Hopo :-)

User object: <User 6>    User ID:  6    Username Matti Meikäläinen

User object: <User 7>    User ID:  7    Username Juha Engineer

User object: <User 11>    User ID:  11    Username Anni McLennox

User object: <User 20>    User ID:  20    Username ;-(( sad cat *//*

 RETURN item (row) WITH PRIMARY KEY

User object: <User 5>    User ID:  5    Username Hessu Hopo :-)

  REMOVE ALL DATABASE

Traceback (most recent call last):
....
sqlite3.OperationalError: no such table: user

The above exception was the direct cause of the following exception:
....
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user

[SQL: SELECT user.id AS user_id, user.user_name AS user_user_name
FROM user]
(Background on this error at: http://sqlalche.me/e/13/e3q8)

"""