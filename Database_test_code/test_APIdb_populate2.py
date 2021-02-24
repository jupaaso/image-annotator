# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# test_APIdb_populate2.py
# testing population of imageAnnoAPI database models of Image Annotator

# run by command - python test_APIdb_populate2.py

"""
In order to run this test code of ImageAnnotator flask API.

Add following files and folders to ImageAnnotator -folder:
* ImageTest -folder including test images from web
* Phototest -folder including test private photos
* imageAnnoAPI.py -file
* python test_APIdb_populate2.py

ImageAnnotator -folder includes also
* .venv -folder (python virtual environment)
* .vscode -folder (VSC launch and settings)

Activate created python virtual environment (on VSC cmd):
cd C:\PWBproject\ImageAnnotator\.venv\Scripts
activate.bat

Go to ImageAnnotator folder:
(.venv) C:\PWBproject\ImageAnnotator>

Run test file by command:
python test_APIdb_populate2.py

TESTING
* This code creates database, 
* and populates User, PhotoContent, and PhotoAnnotation tables
* This test code fails to add user_id on annotation step from user table

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
    print("\n User in database: " + item.user_name)

# Print users without data
userqueried1 = User.query.filter_by(user_name="Meria Developer").first()
userqueried2 = User.query.filter_by(user_name="Juha Engineer").first()
userqueried3 = User.query.filter_by(user_name="Matti Meikäläinen").first()
print("\n user1: ", userqueried1, ", id:", userqueried1.id, "and name: ", userqueried1.user_name)
print("\n user2: ", userqueried2, ", id:", userqueried2.id, "and name: ", userqueried2.user_name)
print("\n user3: ", userqueried3, ", id:", userqueried3.id, "and name: ", userqueried3.user_name)

# -------------------------------------------------------------------

# Testing PhotoContent -model population

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
        print("\nPhoto id:       ", photo.id)
        print("Photo user_id:  ", photo.user_id)
        print("Photo name:     ", photo.name)
        print("Photo date:     ", photo.date)
        print("Photo location: ", photo.location)

# -------------------------------------------------------------------

# Testing PhotoAnnotation -model population

# Collect photos and photo data from defined PhotoTest -folder to photo_list
def getPhotoAnnoData():
    photoAnno_list = []
    thisdict = {
        "persons_class": True,
        "text_persons": "John Doe",
        "text_persons_comment": "Who is this person",
        "text_free_comment": "Photo too weird",
        "positivity_class": 4,
        "slideshow_class": True
    }
    photoAnno_list.append(thisdict)
    return photoAnno_list

# Collect defined photo from database
photoname_queried = PhotoContent.query.filter_by(name="Omakuva.jpg").first()
#print(photoname_queried)
#<PhotoContent 7>

# Add annotations of photoAnno_list for defined photo (name) in database
# and commit to database
anno_list = getPhotoAnnoData()
for anno in anno_list:
    annotation = PhotoAnnotation(persons_class=anno["persons_class"], text_persons=anno["text_persons"], text_persons_comment=anno["text_persons_comment"], text_free_comment=anno["text_free_comment"], positivity_class=anno["positivity_class"], slideshow_class=anno["slideshow_class"])
    photoname_queried.photo_annotations.append(annotation)
    db.session.commit()

# Collect photo data of defined photo from database
results3 = PhotoContent.query.filter_by(name="Omakuva.jpg").first()
print("\nPhoto content:           ", results3)
print("Photo content id:        ", results3.id)
print("Photo content user_id:   ", results3.user_id)

# Collect photo data of defined photo from database
results4 = PhotoAnnotation.query.join(PhotoContent).filter(PhotoContent.name == "Omakuva.jpg").first() 

print("\nPhoto annotation:                        ", results4)
print("Photo annotation id:                     ", results4.id)
print("Photo annotation photo_id:               ", results4.photo_id)
print("Photo annotation user_id:                ", results4.user_id)
print("Photo annotation persons_class:          ", results4.persons_class)
print("Photo annotation text_persons:           ", results4.text_persons)
print("Photo annotation text_persons_comment:   ", results4.text_persons_comment)
print("Photo annotation text_free_comment:      ", results4.text_free_comment)
print("Photo annotation positivity_class:       ", results4.positivity_class)
print("Photo annotation slideshow_class:        ", results4.slideshow_class)


"""
RESULTS  ---------------------------------------------------------------

 User in database: Meria Developer
 User in database: Juha Engineer
 User in database: Matti Meikäläinen

 user1:  <User 1> , id: 1 and name:  Meria Developer
 user2:  <User 2> , id: 2 and name:  Juha Engineer  
 user3:  <User 3> , id: 3 and name:  Matti Meikäläinen

Photos saved by user: Matti Meikäläinen

Photo id:        1
Photo user_id:   3
Photo name:      20200725_215012.jpg
Photo date:      2021-02-24 19:07:45.805001
Photo location:  C:\PWBproject\ImageAnnotator\PhotoTest\20200725_215012.jpg

Photo id:        2
Photo user_id:   3
Photo name:      Iitukka =).JPG
Photo date:      2021-02-24 19:07:45.809988
Photo location:  C:\PWBproject\ImageAnnotator\PhotoTest\Iitukka =).JPG

Photo id:        3
Photo user_id:   3
Photo name:      lampaat tauolla.JPG
Photo date:      2021-02-24 19:07:45.837941
Photo location:  C:\PWBproject\ImageAnnotator\PhotoTest\lampaat tauolla.JPG

Photo id:        4
Photo user_id:   3
Photo name:      Norja 2020.jpg
Photo date:      2021-02-24 19:07:45.843926
Photo location:  C:\PWBproject\ImageAnnotator\PhotoTest\Norja 2020.jpg

Photo id:        5
Photo user_id:   3
Photo name:      Omakuva.jpg
Photo date:      2021-02-24 19:07:45.848914
Photo location:  C:\PWBproject\ImageAnnotator\PhotoTest\Omakuva.jpg

Photo content:            <PhotoContent 5>
Photo content id:         5
Photo content user_id:    3

Photo annotation:                         <PhotoAnnotation 1>
Photo annotation id:                      1
Photo annotation photo_id:                5
Photo annotation user_id:                 None
Photo annotation persons_class:           True
Photo annotation text_persons:            John Doe
Photo annotation text_persons_comment:    Who is this person
Photo annotation text_free_comment:       Photo too weird
Photo annotation positivity_class:        4
Photo annotation slideshow_class:         True

"""