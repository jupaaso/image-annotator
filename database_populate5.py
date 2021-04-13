# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# database_populate5.py

# testing population of imageAnnoAPI database models of Image Annotator

# pip install pillow

"""
In order to run this test code of ImageAnnotator flask API.

Add following files and folders to ImageAnnotator -folder:
* Data -folder - includes ImageTest and Phototest -folders
* this file 'database_populate5.py' next to 'manage.py' -file

Activate created python virtual environment (on VSC cmd):
    cd C:\PWBproject\ImageAnnotator\.venv\Scripts
    activate.bat

Go to ImageAnnotator folder:
    (.venv) C:\PWBproject\ImageAnnotator>

Set cofiguration setting class as 'development' or 'production' or 'default'
    (.venv) C:\PWBproject\ImageAnnotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\PWBproject\ImageAnnotator\extracodes>set FLASK_APP=hub

Run test file by command:
    (.venv) C:\PWBproject\ImageAnnotator>python database_populate5.py

TESTING
* This code creates database models, 
* and populates User, PhotoContent, PhotoAnnotation, ImageContent and ImageAnnotation models

RESULTS
* available at the end of the code

"""

from hub import create_app, db
from hub.models import User, ImageAnnotation, ImageContent, PhotoAnnotation

from datetime import datetime
import glob
import base64
from io import BytesIO
import os
from PIL import Image, ExifTags

config = os.getenv('FLASK_ENV')
print("configuration: ", config)

# -------------------------------------------------------------------
# creates app with defined environment and configuration
app = create_app(os.getenv('FLASK_ENV') or 'default')
with app.app_context():
    db.create_all()

# -------------------------------------------------------------------
# Testing User -model population

# Create new row for new user to database by using User -model
    user1 = User(user_name = "Meria Developer", user_password="mötkäle")
    user2 = User(user_name = "Juha Engineer", user_password="auty8f645bf")
    user3 = User(user_name = "Matti Meikäläinen", user_password="1234567890")
    user4 = User(user_name = "Katti ole' Matikainen", user_password="åäöpolkijju876")
    user5 = User(user_name = "Hessu Hopo :-) ", user_password="K8Hyf43HVruj47")
    user6 = User(user_name = "Juha Engineer", user_password="vl75dJrVh90765d")

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

# -------------------------------------------------------------------
# Testing ImageContent -model population
    print("\nADD images, photos and annotation for defined image/photo name ")

# Collect images and image data from defined ImageTest -folder to image_list
    def getImageData():
        image_list = []
        for filename in glob.glob('C:\\PWBproject\\ImageAnnotator\\data\\ImageTest\\*.jpg'):
            #print("Filename:  ", filename)
            #filedate = os.path.getctime(filename)

            with open(filename, "rb") as f:
                image_binary = f.read()
                imageAscii = base64.b64encode(image_binary).decode('ascii')
                timestamp = os.path.getctime(filename)
                datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

                thisdict = {
                    "data": image_binary,
                    "ascii_data": imageAscii,
                    "name": os.path.basename(filename),
                    "publish_date": datetime.fromisoformat(datetime_str),
                    "location": filename,
                    "is_private": False,
                    "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                }
            image_list.append(thisdict)
        return image_list

# Collect defined user from database
    userqueried = User.query.filter_by(user_name="Meria Developer").first()

# Add images of image_list (collected from defined folder in path) for user in database
# and commit to database
    image_list = getImageData()
    for im in image_list:
        image = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], publish_date=im["publish_date"], location=im["location"], is_private=im["is_private"], date=im["date"])
        print(image.publish_date)
        print(image.date)
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
            print(image.publish_date)
            print(image.location)
            print(image.is_private)
            print(image.date)


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
        for filename in glob.glob('C:\PWBproject\ImageAnnotator\data\PhotoTest/*.jpg'):
            im = Image.open(filename)
            exifdata = im.getexif()
            if exifdata:
                # Make a map with tag names
                exif = { ExifTags.TAGS[k]: v for k, v in exifdata.items() if k in ExifTags.TAGS and type(v) is not bytes }                
                # Grab the date
                date_obj = datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
                print(date_obj)
            else:
                print('Unable to get date from exif for %s' % filename)
            del im
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
#        photo = PhotoContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"])
        photo = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"], is_private=True)
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
    #photoname_queried = PhotoContent.query.filter_by(name="lampaat tauolla.JPG").first()
    photoname_queried = ImageContent.query.filter_by(name="lampaat tauolla.JPG").first()

# and commit both to database
    anno_list = getPhotoAnnoData()
    for anno in anno_list:
        annotation = PhotoAnnotation(persons_class=anno["persons_class"], text_persons=anno["text_persons"], text_persons_comment=anno["text_persons_comment"], text_free_comment=anno["text_free_comment"], positivity_class=anno["positivity_class"], slideshow_class=anno["slideshow_class"])   
        current_user.photo_annotator.append(annotation)
        photoname_queried.photo_annotations.append(annotation)
        db.session.commit()

# Collect photo content data of defined photo from database
#    lammaskuva = PhotoContent.query.filter_by(name="lampaat tauolla.JPG").first()
    lammaskuva = ImageContent.query.filter_by(name="lampaat tauolla.JPG").first()
    print("\nPhoto content:           ", lammaskuva)
    print("Photo content id:        ", lammaskuva.id)
    print("Photo content user_id:   ", lammaskuva.user_id)

# Collect photo annotation data of defined photo from database
    lampaat_annotoitu = PhotoAnnotation.query.join(ImageContent).filter(ImageContent.name == "lampaat tauolla.JPG").first() 
    #lampaat_annotoitu = PhotoAnnotation.query.join(PhotoContent).filter(PhotoContent.name == "lampaat tauolla.JPG").first() 

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
