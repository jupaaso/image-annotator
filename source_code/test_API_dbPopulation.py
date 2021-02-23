# PWB course 2021
# Image annotator testing database population
# test_API_dbPopulation.py
# python test_API_dbPopulation.py

from imageAnnoAPI import db
from imageAnnoAPI import ImageContent, PhotoContent, ImageAnnotation, PhotoAnnotation, User

from datetime import datetime

# -------------------------------------------------------------------
"""
user1 = User(user_name = "Meria Developer")
user2 = User(user_name = "Juha Engineer")
user3 = User(user_name = "Matti Meikäläinen")

# user4 = User(user_name"Just Testing")         # invalid syntax

# long string list does not cause error message
#user4 = User(user_name = "Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen")

# no name does not cause error message
#user4 = User(user_name = "")

# syntax error
#user4 = User(user_name =  )

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)

db.session.commit()

results = User.query.all()

for item in results:
    print(item.user_name)
"""

import glob
import base64
from io import BytesIO
import os

def getImageData():
    image_list = []
    for filename in glob.glob('C:\PWBproject\ImageAnnotator\ImageDownload\ImageTest/*.jpg'):
        print(filename)

        with open(filename, "rb") as f:
            image_binary = f.read()
            imageAscii = base64.b64encode(image_binary).decode('ascii') 

            thisdict = {
                "data": image_binary,
                "ascii_data": imageAscii,
                "name": os.path.basename(filename),
                "date": datetime.now(),
                "location":filename
            }
        image_list.append(thisdict)
    return image_list

# lataa kuvat käyttäjälle

user1 = User(user_name = "Meria Developer")
user2 = User(user_name = "Juha Engineer")
user3 = User(user_name = "Matti Meikäläinen")
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

# hae tietty käyttäjä
userqueried = User.query.filter_by(user_name="Meria Developer").first()

image_list = getImageData()
for im in image_list:
    image = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"])
    userqueried.image_user.append(image)
    db.session.commit()

results = User.query.filter_by(user_name="Meria Developer").all()

for item in results:
    print("images saved by user: " + item.user_name)
    for image in item.image_user:
        print(image.name)
        print(image.date)
        print(image.location)


# --------------------------------------------------------------
# FLASK_APP=test_API_dbPopulation
# python -m flask run [OPTIONS]

# PWB course 2021
# Image annotator testing database population
# test_API_dbPopulation.py
# python test_API_dbPopulation.py

from imageAnnoAPI import db
from imageAnnoAPI import ImageContent, PhotoContent, ImageAnnotation, PhotoAnnotation, User

from datetime import datetime

# -------------------------------------------------------------------
"""
user1 = User(user_name = "Meria Developer")
user2 = User(user_name = "Juha Engineer")
user3 = User(user_name = "Matti Meikäläinen")

# user4 = User(user_name"Just Testing")         # invalid syntax

# long string list does not cause error message
#user4 = User(user_name = "Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen Katti Matikainen")

# no name does not cause error message
#user4 = User(user_name = "")

# syntax error
#user4 = User(user_name =  )

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)

db.session.commit()

results = User.query.all()

for item in results:
    print(item.user_name)
"""

import glob
import base64
from io import BytesIO
import os

def getImageData():
    image_list = []
    for filename in glob.glob('C:\PWBproject\ImageAnnotator\ImageDownload\ImageTest/*.jpg'):
        print(filename)

        with open(filename, "rb") as f:
            image_binary = f.read()
            imageAscii = base64.b64encode(image_binary).decode('ascii') 

            thisdict = {
                "data": image_binary,
                "ascii_data": imageAscii,
                "name": os.path.basename(filename),
                "date": datetime.now(),
                "location":filename
            }
        image_list.append(thisdict)
    return image_list

# lataa kuvat käyttäjälle

user1 = User(user_name = "Meria Developer")
user2 = User(user_name = "Juha Engineer")
user3 = User(user_name = "Matti Meikäläinen")
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

# hae tietty käyttäjä
userqueried = User.query.filter_by(user_name="Meria Developer").first()

image_list = getImageData()
for im in image_list:
    image = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"])
    userqueried.image_user.append(image)
    db.session.commit()

results = User.query.filter_by(user_name="Meria Developer").all()

for item in results:
    print("images saved by user: " + item.user_name)
    for image in item.image_user:
        print(image.name)
        print(image.date)
        print(image.location)


# --------------------------------------------------------------
# FLASK_APP=test_API_dbPopulation
# python -m flask run [OPTIONS]

