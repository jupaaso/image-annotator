# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso
# Image Annotator API database models - models.py
# This file includes database models of Image Annotator API.

# ---------------------------------------------------------------------------
# check / change launch.json -file parameters and location 
# if debugging with VSC and Postman
# ----------------------------------------------------------------------------
# The first time the app runs it creates the table. 
# BE CAREFULL - With this code you can override the default table name
# ----------------------------------------------------------------------------
import os
import glob
import base64
from io import BytesIO

from datetime import datetime
import click
from flask.cli import with_appcontext
from hub import db
from hub.constants import *


# database model for image content and photo content ------------------------------------------

class ImageContent(db.Model):
    __tablename__ = 'imagecontent'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    data = db.Column(db.LargeBinary, nullable=False)
    ascii_data = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    publish_date = db.Column(db.DateTime, nullable = True)
    location = db.Column(db.String(64), nullable=False)
    is_private = db.Column(db.Boolean(), default=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    image_annotations = db.relationship("ImageAnnotation", back_populates="image")
    # img_user on lista - eri nimi ja kätetäänkö listoina - imageUsers
    img_user = db.relationship("User", back_populates="image_user", uselist=True)
    photo_annotations = db.relationship("PhotoAnnotation", back_populates="photo")
    # photoUsers
    pho_user = db.relationship("User", back_populates="photo_user", uselist=True)


# database model for imageannotation ---------------------------------------------------

class ImageAnnotation(db.Model):
    __tablename__ = 'imageannotation'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey("imagecontent.id", ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    # three boolean classifiers
    meme_class = db.Column(db.Boolean, nullable=False)
    HS_class= db.Column(db.Boolean, nullable=False)
    text_class = db.Column(db.Boolean, nullable=False)
    # pos-neg polarity classifiers
    polarity_classA = db.Column(db.Integer, nullable=True)
    polarity_classB = db.Column(db.Integer, nullable=True)
    # HS classifiers
    HS_strength = db.Column(db.Integer, nullable=True)
    HS_category = db.Column(db.String(128), nullable=True)
    # text classifiers
    text_text = db.Column(db.String(300), nullable=True)
    text_language = db.Column(db.String(64), nullable=True)

    # images
    image = db.relationship("ImageContent", back_populates="image_annotations", uselist=True)
    # imageAnnotators
    img_annotator = db.relationship("User", back_populates="image_annotator", uselist=True)


# database model for photoannotation ---------------------------------------------------

class PhotoAnnotation(db.Model):
    __tablename__ = 'photoannotation'

    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey("imagecontent.id", ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    # boolean classifiers
    persons_class = db.Column(db.Boolean, nullable=False)
    slideshow_class = db.Column(db.Boolean, nullable=False)
    # pos value classifier
    positivity_class = db.Column(db.Integer, nullable=False)
    # text classifiers
    text_free_comment = db.Column(db.String(128), nullable=True)
    text_persons = db.Column(db.String(128), nullable=True)
    text_persons_comment = db.Column(db.String(128), nullable=True)

    # geografical location - not sure yet how to do

    photo = db.relationship("ImageContent", back_populates="photo_annotations", uselist=True)
    pho_annotator = db.relationship("User", back_populates="photo_annotator", uselist=True)


# database model for user -----------------------------------------------------------
# user name is unique
# password is not necessary

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128), unique=True, nullable=False)
    user_password = db.Column(db.String(32), nullable=True)

    image_user = db.relationship("ImageContent", back_populates="img_user")
    photo_user = db.relationship("ImageContent", back_populates="pho_user")

    image_annotator = db.relationship("ImageAnnotation", back_populates="img_annotator")
    photo_annotator = db.relationship("PhotoAnnotation", back_populates="pho_annotator")


# start ----------------------------------------------------------------------------
# run this after set FLASK_ENV=development (or testing)
# set FLASk_APP=hub
# flask init-db

@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()

# after running init-db (above)
# run this by 
# flask populate-db
@click.command("populate-db")
@with_appcontext
def generate_test_data():
    import datetime
    import random        
    
    upload = create_static_folder()

    user1 = User(user_name = "Meria Developer", user_password="mötkäle")
    user2 = User(user_name = "Juhis von Engineer", user_password="auty8f645bf")
    user3 = User(user_name = "Matti Meikäläinen", user_password="1234567890")
    user4 = User(user_name = "Katti ole' Matikainen", user_password="åäöpolkijju876")
    user5 = User(user_name = "Hessu Hopo :-) ", user_password="K8Hyf43HVruj47")
    user6 = User(user_name = "Jussi Engineer", user_password="vl75dJrVh90765d")

    # Add model to the session
    db.session.add_all([user1, user2, user3, user4, user5])

    # Save session to database with commit
    db.session.commit()

    # Collect defined user from database
    userqueried = User.query.filter_by(user_name="Meria Developer").first()

# Add images of image_list (collected from defined folder in path) for user in database
# and commit to database
    image_list = getImageData(upload)
    for im in image_list:
        image = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], publish_date=im["publish_date"], location=im["location"], is_private=im["is_private"], date=im["date"])
        print(image.publish_date)
        print(image.date)
        userqueried.image_user.append(image)
        db.session.commit()

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

# Collect defined user from database
    userqueried = User.query.filter_by(user_name="Matti Meikäläinen").first()

# Add photos of photo_list (collected from defined folder in path) for user in database
# and commit to database
    photo_list = getPhotoData(upload)
    for im in photo_list:
#        photo = PhotoContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"])
        photo = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"], is_private=True)
        userqueried.photo_user.append(photo)
        db.session.commit()

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

#####################################################        
def create_static_folder():
    basedir = os.path.abspath(os.path.dirname(__file__))
    upload = basedir + UPLOAD_FOLDER
    try:        
        if not os.path.exists(upload):
            os.makedirs(upload)
    except OSError as e:
        print('FAILED : ' + str(upload), file=sys.stderr)
        raise ValueError('Folder for static iamges could not be created.')
    return upload

# Collect images and image data from defined ImageTest -folder to image_list
def getImageData(upload):
    image_list = []
    source_images_folder = "C:\\PWBproject\\ImageAnnotator\\data\\ImageTest\\"
    for filename in glob.glob(source_images_folder + '*.jpg'):
        print("Filename:  ", filename)
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
                "location": save_to_upload(upload, source_images_folder, os.path.basename(filename)),
                "is_private": False,
                "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
        image_list.append(thisdict)
    return image_list

def save_to_upload(target_folder, source_folder, source_filename):
     # collect the filename
    from shutil import copy        
    
    full_path = os.path.join(source_folder, source_filename)
            
    # copy file from source location to target location
    copy(full_path, target_folder) 
    return str(os.path.join(UPLOAD_FOLDER, source_filename))

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

# Collect photos and photo data from defined PhotoTest -folder to photo_list
def getPhotoData(upload):
    from PIL import Image, ExifTags

    photo_list = []
    source_photos_folder = 'C:\PWBproject\ImageAnnotator\data\PhotoTest/'
    for filename in glob.glob(source_photos_folder + '*.jpg'):
        im = Image.open(filename)
        # default publish_date to None
        publish_date = None
        exifdata = im.getexif()
        if exifdata:
            # Make a map with tag names
            exif = { ExifTags.TAGS[k]: v for k, v in exifdata.items() if k in ExifTags.TAGS and type(v) is not bytes }                
            # Grab the date
            try:
                publish_date = datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
            except Exception as e:
                print('Unable to get DateTimeOriginal from exif for %s' % filename)            
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
                "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "location":save_to_upload(upload, source_photos_folder, os.path.basename(filename)),
                "publish_date": publish_date
            }
        photo_list.append(thisdict)
    return photo_list

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
