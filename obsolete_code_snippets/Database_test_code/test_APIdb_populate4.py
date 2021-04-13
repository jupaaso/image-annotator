# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# test_APIdb_populate4.py

# testing population of imageAnnoAPI database models of Image Annotator

"""
In order to run this test code of ImageAnnotator flask API.

Add following files and folders to ImageAnnotator -folder:
* ImageTest -folder including test images from web
* Phototest -folder including test private photos
* imageAnnoAPI.py -file
* test_APIdb_populate4.py

ImageAnnotator -folder includes also
* .venv -folder (python virtual environment)
* .vscode -folder (VSC launch and settings)

Activate created python virtual environment (on VSC cmd):
    cd C:\PWBproject\ImageAnnotator\.venv\Scripts
    activate.bat

Go to ImageAnnotator folder:
    (.venv) C:\PWBproject\ImageAnnotator>

Run test file by command:
    python test_APIdb_populate4.py

TESTING
* This code creates database models, 
* and populates User, PhotoContent, PhotoAnnotation, ImageContent and ImageAnnotation models

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

# Create new row for new user to database by using User -model
user1 = User(user_name = "Meria Developer")
user2 = User(user_name = "Juha Engineer")
user3 = User(user_name = "Matti Meikäläinen")
user4 = User(user_name = "Katti ole' Matikainen")
user5 = User(user_name = "Hessu Hopo :-) ")
user6 = User(user_name = "Juha Engineer")

# Add model to the session
db.session.add_all([user1, user2, user3, user4, user5, user6])

# Save session to database with commit
db.session.commit()

print("\nADD USER \n")

# Execute SQL query for database by using Model.query
# OR for db.session.query(Model)
# query.all() get all rows in the database as a list
result_users = User.query.all()
for item in result_users:
    print("User object:  ", item ,"   User ID: ", item.id, "   Username:  ", item.user_name)

print("\nADD images, photos and annotation for defined image/photo name ")

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

"""
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
"""
# -------------------------------------------------------------------
# Testing ImageAnnotation -model population

def getImageAnnoData():
    imageAnno_list = []
    thisdict = {
        "meme_class": True,
        "HS_class": False,
        "text_class": True,
        "polarity_classA": -1,
        "polarity_classB": -3,
        "HS_strength": -2,
        "HS_category": "bully",
        "text_text": "Tähän jotain suomenkielistä tekstiä ;-)))) !!",
        "text_language": "finnish"
    }
    imageAnno_list.append(thisdict)
    return imageAnno_list

# collect queries for defined user_name and photo name
current_User = User.query.filter_by(user_name="Meria Developer").first()
imagename_queried = ImageContent.query.filter_by(name="kuha meemi1.jpg").first()

# and commit both to database
Im_anno_list = getImageAnnoData()
for anno in Im_anno_list:
    annotation = ImageAnnotation(meme_class=anno["meme_class"], 
                                HS_class=anno["HS_class"], 
                                text_class=anno["text_class"], 
                                polarity_classA=anno["polarity_classA"], 
                                polarity_classB=anno["polarity_classB"], 
                                HS_strength=anno["HS_strength"],
                                HS_category=anno["HS_category"],
                                text_text=anno["text_text"],
                                text_language=anno["text_language"])   
    current_User.image_annotator.append(annotation)
    imagename_queried.image_annotations.append(annotation)
    db.session.commit()

# Collect image content data of defined image from database
kuhakuva = ImageContent.query.filter_by(name="kuha meemi1.jpg").first()
print("\nImage content:           ", kuhakuva)
print("Image content id:        ", kuhakuva.id)
print("Image content user_id:   ", kuhakuva.user_id)

# Collect image annotation data of defined image from database
kuhakuva_annotoitu = ImageAnnotation.query.join(ImageContent).filter(ImageContent.name == "kuha meemi1.jpg").first() 

print("\nImage annotation:                    ", kuhakuva_annotoitu)
print("Image annotation id:                 ", kuhakuva_annotoitu.id)
print("Image annotation image_id:           ", kuhakuva_annotoitu.image_id)
print("Image annotation user_id:            ", kuhakuva_annotoitu.user_id)
print("Image annotation meme_class:         ", kuhakuva_annotoitu.meme_class)
print("Image annotation HS_class:           ", kuhakuva_annotoitu.HS_class)
print("Image annotation text_class:         ", kuhakuva_annotoitu.text_class)
print("Image annotation polarity_classA:    ", kuhakuva_annotoitu.polarity_classA)
print("Image annotation polarity_classB:    ", kuhakuva_annotoitu.polarity_classB)
print("Image annotation HS_strength:        ", kuhakuva_annotoitu.HS_strength)
print("Image annotation HS_category:        ", kuhakuva_annotoitu.HS_category)
print("Image annotation text_text:          ", kuhakuva_annotoitu.text_text)
print("Image annotation text_language:      ", kuhakuva_annotoitu.text_language)

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

"""
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
"""
# -------------------------------------------------------------------
# Testing PhotoAnnotation -model population

def getPhotoAnnoData():
    photoAnno_list = []
    thisdict = {
        "persons_class": True,
        "text_persons": "Lampaita",
        "text_persons_comment": "Lampaita laitumella",
        "text_free_comment": "Kesäkuva",
        "positivity_class": 4,
        "slideshow_class": True
    }
    photoAnno_list.append(thisdict)
    return photoAnno_list

# collect queries for defined user_name and photo name
current_user = User.query.filter_by(user_name="Matti Meikäläinen").first()
photoname_queried = PhotoContent.query.filter_by(name="lampaat tauolla.JPG").first()

# and commit both to database
anno_list = getPhotoAnnoData()
for anno in anno_list:
    annotation = PhotoAnnotation(persons_class=anno["persons_class"], text_persons=anno["text_persons"], text_persons_comment=anno["text_persons_comment"], text_free_comment=anno["text_free_comment"], positivity_class=anno["positivity_class"], slideshow_class=anno["slideshow_class"])   
    current_user.photo_annotator.append(annotation)
    photoname_queried.photo_annotations.append(annotation)
    db.session.commit()

# Collect photo content data of defined photo from database
lammaskuva = PhotoContent.query.filter_by(name="lampaat tauolla.JPG").first()
print("\nPhoto content:           ", lammaskuva)
print("Photo content id:        ", lammaskuva.id)
print("Photo content user_id:   ", lammaskuva.user_id)

# Collect photo annotation data of defined photo from database
lampaat_annotoitu = PhotoAnnotation.query.join(PhotoContent).filter(PhotoContent.name == "lampaat tauolla.JPG").first() 

print("\nPhoto annotation:                        ", lampaat_annotoitu)
print("Photo annotation id:                     ", lampaat_annotoitu.id)
print("Photo annotation photo_id:               ", lampaat_annotoitu.photo_id)
print("Photo annotation user_id:                ", lampaat_annotoitu.user_id)
print("Photo annotation persons_class:          ", lampaat_annotoitu.persons_class)
print("Photo annotation text_persons:           ", lampaat_annotoitu.text_persons)
print("Photo annotation text_persons_comment:   ", lampaat_annotoitu.text_persons_comment)
print("Photo annotation text_free_comment:      ", lampaat_annotoitu.text_free_comment)
print("Photo annotation positivity_class:       ", lampaat_annotoitu.positivity_class)
print("Photo annotation slideshow_class:        ", lampaat_annotoitu.slideshow_class)


"""
RESULTS  ---------------------------------------------------------------

ADD USER 

User object:   <User 1>    User ID:  1    Username:   Meria Developer
User object:   <User 2>    User ID:  2    Username:   Juha Engineer
User object:   <User 3>    User ID:  3    Username:   Matti Meikäläinen
User object:   <User 4>    User ID:  4    Username:   Katti ole' Matikainen
User object:   <User 5>    User ID:  5    Username:   Hessu Hopo :-)
User object:   <User 6>    User ID:  6    Username:   Juha Engineer

ADD images, photos and annotation for defined image/photo name

Image content:            <ImageContent 2>
Image content id:         2
Image content user_id:    1

Image annotation:                     <ImageAnnotation 1>
Image annotation id:                  1
Image annotation image_id:            2
Image annotation user_id:             1
Image annotation meme_class:          True
Image annotation HS_class:            False
Image annotation text_class:          True
Image annotation polarity_classA:     -1
Image annotation polarity_classB:     -3
Image annotation HS_strength:         -2
Image annotation HS_category:         bully
Image annotation text_text:           Tähän jotain suomenkielistä tekstiä ;-)))) !!
Image annotation text_language:       finnish

Photo content:            <PhotoContent 3>
Photo content id:         3
Photo content user_id:    3

Photo annotation:                         <PhotoAnnotation 1>
Photo annotation id:                      1
Photo annotation photo_id:                3
Photo annotation user_id:                 3
Photo annotation persons_class:           True
Photo annotation text_persons:            Lampaita
Photo annotation text_persons_comment:    Lampaita laitumella
Photo annotation text_free_comment:       Kesäkuva
Photo annotation positivity_class:        4
Photo annotation slideshow_class:         True

"""