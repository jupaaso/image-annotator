# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# Image Annotator API database models - models.py
# This file includes database models of Image Annotator API.

# check / change launch.json -file parameters and location if debugging with VSC or Postman

# --------------------------------------------------------------------------------------------

# The first time the app runs it creates the table. 
# BE CAREFULL - With this code you can override the default table name

# cd C:\PWPproject\ImageAnnotator\.venv\Scripts
# activate.bat
# C:\PWPproject\ImageAnnotator>
# set FLASK_ENV=development (or testing)
# set FLASK_APP=hub
# flask init-db
# flask populate-db
# flask run

# --------------------------------------------------------------------------------------------
"""
In order run ImageAnnotator flask API and this file 
activate virtual environment, set flask, init database and populate database.

Activate created python virtual environment (on cmd):
    cd C:\PWPproject\ImageAnnotator\.venv\Scripts
    activate.bat

Go to ImageAnnotator folder: (provide 'cd ..' on cmd)
    (.venv) C:\PWPproject\ImageAnnotator>

Set cofiguration setting class as 'development' or 'production' or 'default' or 'testing'
    (.venv) C:\PWPproject\ImageAnnotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\PWPproject\ImageAnnotator>set FLASK_APP=hub

Init flask database basedir hub:
    (.venv) C:\PWPproject\ImageAnnotator>flask init-db

Populate flask database:
    (.venv) C:\PWPproject\ImageAnnotator>flask populate-db

Run flask local host at http://localhost:5000/admin/

    (.venv) C:\PWPproject\ImageAnnotator>flask run

This code creates database models, 
and populates User, PhotoContent, PhotoAnnotation, ImageContent and ImageAnnotation models
"""
# --------------------------------------------------------------------------------------------

import os
import sys
import glob
#import base64
from io import BytesIO

from datetime import datetime
#import random  

import click
from flask.cli import with_appcontext

from shutil import copy
from PIL import Image, ExifTags

from hub import db
from hub.constants import *
from hub.utils import set_photo_meta_data_to_dict

# database model for image content and photo content -----------------------------------------

class ImageContent(db.Model):
    __tablename__ = 'imagecontent'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    name = db.Column(db.String(128), nullable=False)
    publish_date = db.Column(db.DateTime, nullable = True)
    location = db.Column(db.String(64), nullable=False)
    is_private = db.Column(db.Boolean(), default=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    image_annotations = db.relationship("ImageAnnotation", back_populates="images")
    image_users = db.relationship("User", back_populates="image_user", uselist=True)
    photo_annotations = db.relationship("PhotoAnnotation", back_populates="photos")
    photo_users = db.relationship("User", back_populates="photo_user", uselist=True)

# database model for imageannotation ---------------------------------------------------------

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

    images = db.relationship("ImageContent", back_populates="image_annotations", uselist=True)
    image_annotators = db.relationship("User", back_populates="image_annotator", uselist=True)

# database model for photoannotation --------------------------------------------------------

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
    # geografical location - not created

    photos = db.relationship("ImageContent", back_populates="photo_annotations", uselist=True)
    photo_annotators = db.relationship("User", back_populates="photo_annotator", uselist=True)

# database model for user -------------------------------------------------------------------
# user name is unique - password is not necessary - CHECK CLIENT !!!!!

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128), unique=True, nullable=False)
    user_password = db.Column(db.String(32), nullable=True)

    image_user = db.relationship("ImageContent", back_populates="image_users")
    photo_user = db.relationship("ImageContent", back_populates="photo_users")

    image_annotator = db.relationship("ImageAnnotation", back_populates="image_annotators")
    photo_annotator = db.relationship("PhotoAnnotation", back_populates="photo_annotators")


# --------------------------------------------------------------------------------------------
# HELPER FUNCTIONS - CLICK COMMANDS
# create database and popuate it for test and dvelopment purposes

@click.command("init-db")
@with_appcontext

def init_db_command():
    db.create_all()

@click.command("populate-db")
@with_appcontext


def generate_test_data():

    (upload_images_folder, upload_photos_folder) = create_static_folders()

    # Create row for new user to database by using User -model
    user1 = User(user_name = "Meria Developer", user_password="mötkäle")
    user2 = User(user_name = "Juhis von Engineer", user_password="auty8f645bf")
    user3 = User(user_name = "Matti Meikäläinen", user_password="1234567890")
    user4 = User(user_name = "Katti ole' Matikainen", user_password="åäöpolkijju876")
    user5 = User(user_name = "Hassu Hooponen :-) ", user_password="K8Hyf43HVruj47")
    user6 = User(user_name = "Jussi Engineer", user_password="vl75dJrVh90765d")
    # Add model to the session
    db.session.add_all([user1, user2, user3, user4, user5, user6])
    # Save session to database with commit
    db.session.commit()

    # Collect defined user from database
    userqueried = User.query.filter_by(user_name="Meria Developer").first()

    # Add images of image_list (collected from defined folder in path) for defined user in database
    # and commit to database
    image_list = getImageData(upload_images_folder)
    for im in image_list:
        image = ImageContent(name=im["name"], publish_date=im["publish_date"], location=im["location"], is_private=im["is_private"], date=im["date"])
        #print(image.publish_date)
        #print(image.date)
        userqueried.image_user.append(image)
        db.session.commit()

    # Queries to collect defined user_name and photo name from database
    current_User = User.query.filter_by(user_name="Meria Developer").first()
    imagename_queried = ImageContent.query.filter_by(name="kuha meemi1.jpg").first()

    # Append and commit image annotation data for both to database
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
    photo_list = getPhotoData(upload_photos_folder)
    for im in photo_list:
        # photo = PhotoContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"])
        photo = ImageContent(name=im["name"], date=im["date"], location=im["location"], is_private=True)
        userqueried.photo_user.append(photo)
        db.session.commit()

    # collect queries for defined user_name and photo name
    current_user = User.query.filter_by(user_name="Matti Meikäläinen").first()
    photoname_queried = ImageContent.query.filter_by(name="lampaat tauolla.JPG").first()

    # and commit both to database
    anno_list = getPhotoAnnoData()
    for anno in anno_list:
        annotation = PhotoAnnotation(persons_class=anno["persons_class"], text_persons=anno["text_persons"], text_persons_comment=anno["text_persons_comment"], text_free_comment=anno["text_free_comment"], positivity_class=anno["positivity_class"], slideshow_class=anno["slideshow_class"])   
        current_user.photo_annotator.append(annotation)
        photoname_queried.photo_annotations.append(annotation)
        db.session.commit()

# -------------------------------------------------------------------------------
# Create images and photos folders to static folder in hub

def create_static_folders():    
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        upload_images = basedir + UPLOAD_FOLDER_IMAGES
        if not os.path.exists(upload_images):
            os.makedirs(upload_images)
    except OSError as e:
        print('FAILED : ' + str(upload_images), file=sys.stderr)
        raise ValueError('Folder for static images could not be created.')
    try:
        upload_photos = basedir + UPLOAD_FOLDER_PHOTOS
        if not os.path.exists(upload_photos):
            os.makedirs(upload_photos)
    except OSError as e:
        print('FAILED : ' + str(upload_photos), file=sys.stderr)
        raise ValueError('Folder for static photos could not be created.')
    return (upload_images, upload_photos)

# -------------------------------------------------------------------------------
# Collect filename and location of image/photo files
# from shutil import copy   

def save_to_upload(target_folder, source_folder, source_filename):
    
    # collect the filename
    full_path = os.path.join(source_folder, source_filename)
            
    # copy file from source location to target location
    copy(full_path, target_folder)
    if UPLOAD_FOLDER_IMAGES in target_folder:
        return str(os.path.join(UPLOAD_FOLDER_IMAGES, source_filename))
    if UPLOAD_FOLDER_PHOTOS in target_folder:
        return str(os.path.join(UPLOAD_FOLDER_PHOTOS, source_filename))

# -------------------------------------------------------------------------------
# Collect images and image meta data from defined ImageTest -folder to image_list

# NOTE!!!
# remember to set image location, this is done differently in tests (test images folder -> static/images)
# in development state image is saved from request (request.image -> static/images)

# NOTE ! is_private = False

def getImageData(upload):
    image_list = []

    # DO NOT USE absolut path
    #source_images_folder = "C:\\PWPproject\\ImageAnnotator\\data\\ImageTest\\"
    # USE relative path
    cwd = os.getcwd()
    folder = '\\data\\ImageTest\\'
    source_images_folder = cwd + folder
    print("Print of models.py -file : source_images_folder:", source_images_folder)
    
    for filename in glob.glob(source_images_folder + '*.jpg'):
        #print("\n Print image data filename:  ", filename)
        #filedate = os.path.getctime(filename)

        with open(filename, "rb") as f:
            timestamp = os.path.getctime(filename)
            datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            thisdict = {
                "name": os.path.basename(filename),
                "publish_date": datetime.fromisoformat(datetime_str),
                "location": save_to_upload(upload, source_images_folder, os.path.basename(filename)),
                "is_private": False,
                "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
        image_list.append(thisdict)
    return image_list

# Define image annotation data for database test population
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

# -------------------------------------------------------------------------------
# Collect photos and photo meta data from defined PhotoTest -folder to photo_list

# from PIL import Image, ExifTags

# NOTE!!!
# remember to set photo location, this is done differently in tests (test photo folder -> static/photos)
# in development state photo is saved from request (request.image -> static/photos)

# NOTE ! is_private = True

def getPhotoData(upload):
    photo_list = []

    # DO NOT USE absolut path
    # source_photos_folder = 'C:\\PWPproject\\ImageAnnotator\\data\\PhotoTest//'
    # USE relative path
    cwd = os.getcwd()
    folder = '\\data\\PhotoTest\\'
    source_photos_folder = cwd + folder
    print("Print of models.py -file : source_photos_folder:", source_photos_folder)
    
    for filename in glob.glob(source_photos_folder + '*.jpg'):        
        meta_data_dict = set_photo_meta_data_to_dict(filename, True)
        meta_data_dict["location"] = save_to_upload(upload, source_photos_folder, os.path.basename(filename))
        photo_list.append(meta_data_dict)
    return photo_list

# Define photo annotation data for database PhotoAnnotation -model population
def getPhotoAnnoData():
    photoAnno_list = []
    thisdict = {
        "persons_class": True,
        "slideshow_class": True,
        "positivity_class": 4,
        "text_free_comment": "Norway on summer 2020",
        "text_persons": "norwegian sheep",
        "text_persons_comment": "Norwegian sheep having a nap on shore"
    }
    photoAnno_list.append(thisdict)
    return photoAnno_list

# -------------------------------------------------------------------------------