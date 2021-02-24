# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# test_APIdb_populate1.py
# testing population of imageAnnoAPI database models of Image Annotator

# run by command - python test_APIdb_populate1.py

"""
In order to run this test code of ImageAnnotator flask API.

Add following files and folders to ImageAnnotator -folder:
* ImageTest -folder including test images from web
* Phototest -folder including test private photos
* imageAnnoAPI.py -file
* python test_APIdb_populate1.py

ImageAnnotator -folder includes also
* .venv -folder (python virtual environment)
* .vscode -folder (VSC launch and settings)

Activate created python virtual environment (on VSC cmd):
cd C:\PWBproject\ImageAnnotator\.venv\Scripts
activate.bat

Go to ImageAnnotator folder:
(.venv) C:\PWBproject\ImageAnnotator>

Run test file by command:
python test_APIdb_populate1.py

TESTING
* This code creates database, 
* and populates User, ImageContent, and PhotoContent tables

RESULTS
* available in the end of the code

"""

from imageAnnoAPI import db
from imageAnnoAPI import ImageContent, PhotoContent, ImageAnnotation, PhotoAnnotation, User

from datetime import datetime
import glob
import base64
from io import BytesIO
import os

# -------------------------------------------------------------------

# Testing User -model population

# Create new users to database
user1 = User(user_name = "Meria Developer")
user2 = User(user_name = "Juha Engineer")
user3 = User(user_name = "Matti Meikäläinen")
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

result_users = User.query.all()

for item in result_users:
    print("\nUser in database: " + item.user_name)

# -------------------------------------------------------------------

# Testing ImageContent -model population

# Collect images and image data from defined ImageTest -folder to image_list
def getImageData():
    image_list = []
    for filename in glob.glob('C:\PWBproject\ImageAnnotator\ImageTest/*.jpg'):
        #print(filename)

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

# Collect defined user from database
userqueried = User.query.filter_by(user_name="Meria Developer").first()

# Add images of image_list (collected from defined folder in path) for user in database
# and commit to database
image_list = getImageData()
for im in image_list:
    image = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"])
    userqueried.image_user.append(image)
    db.session.commit()

# Collect image data of defined user from database
results1 = User.query.filter_by(user_name="Meria Developer").all()

# Print image data (name of image, date of image input, location of image input)
# of defined user in database
for item in results1:
    print("\nImages saved by user: " + item.user_name)
    for image in item.image_user:
        print("\n")
        print(image.name)
        print(image.date)
        print(image.location)

# --------------------------------------------------------------

# Testing PhotoContent -model population

# Testing photo name types
# Names of photos in PhotoTest -folder include different name types

# Collect photos and photo data from defined PhotoTest -folder to photo_list
def getPhotoData():
    photo_list = []
    for filename in glob.glob('C:\PWBproject\ImageAnnotator\PhotoTest/*.jpg'):
        #print(filename)

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
        photo_list.append(thisdict)
    return photo_list

# Collect defined user from database
userqueried = User.query.filter_by(user_name="Matti Meikäläinen").first()

# Add photos of photo_list (collected from defined folder in path) for user in database
# and commit to database
photo_list = getPhotoData()
for im in photo_list:
    photo = PhotoContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"])
    userqueried.photo_user.append(photo)
    db.session.commit()

# Collect image data of defined user from database
results2 = User.query.filter_by(user_name="Matti Meikäläinen").all()

# Print image data (name of image, date of image input, location of image input)
# of defined user in database
for item in results2:
    print("\nPhotos saved by user: " + item.user_name)
    for photo in item.photo_user:
        print("\n")
        print(photo.name)
        print(photo.date)
        print(photo.location)

"""
RESULTS  ---------------------------------------------------------------

User in database: Meria Developer
User in database: Juha Engineer
User in database: Matti Meikäläinen

Images saved by user: Meria Developer

halla-aho meemi32.jpg
2021-02-24 19:04:29.223310
C:\PWBproject\ImageAnnotator\ImageTest\halla-aho meemi32.jpg

kuha meemi1.jpg
2021-02-24 19:04:29.223310
C:\PWBproject\ImageAnnotator\ImageTest\kuha meemi1.jpg

kuha meemi3.jpg
2021-02-24 19:04:29.224307
C:\PWBproject\ImageAnnotator\ImageTest\kuha meemi3.jpg

vihreät meemi16.jpg
2021-02-24 19:04:29.224307
C:\PWBproject\ImageAnnotator\ImageTest\vihreät meemi16.jpg

vihreät meemi77.jpg
2021-02-24 19:04:29.224307
C:\PWBproject\ImageAnnotator\ImageTest\vihreät meemi77.jpg

Photos saved by user: Matti Meikäläinen

20200725_215012.jpg
2021-02-24 19:04:29.314511
C:\PWBproject\ImageAnnotator\PhotoTest\20200725_215012.jpg

Iitukka =).JPG
2021-02-24 19:04:29.319497
C:\PWBproject\ImageAnnotator\PhotoTest\Iitukka =).JPG

lampaat tauolla.JPG
2021-02-24 19:04:29.346453
C:\PWBproject\ImageAnnotator\PhotoTest\lampaat tauolla.JPG

Norja 2020.jpg
2021-02-24 19:04:29.353434
C:\PWBproject\ImageAnnotator\PhotoTest\Norja 2020.jpg

Omakuva.jpg
2021-02-24 19:04:29.358421
C:\PWBproject\ImageAnnotator\PhotoTest\Omakuva.jpg

"""
