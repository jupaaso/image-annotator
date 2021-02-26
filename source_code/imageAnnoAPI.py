# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# Image Annotator database model
# imageAnnoAPI.py

# This file includes imageAnnoAPI database models of Image Annotator,
# and creates database when run by test files
# OR
# run by command - python imageAnnoAPI.py

"""
In order to run this file of ImageAnnotator flask API.

Add following files and folders to ImageAnnotator -folder:
* imageAnnoAPI.py -file

ImageAnnotator -folder includes also
* .venv -folder (python virtual environment)
* .vscode -folder (VSC launch and settings)

----------------------------------------------
Activate created python virtual environment (on VSC cmd):
cd C:\PWBproject\ImageAnnotator\.venv\Scripts
activate.bat
# ---- OR
C:\PWBproject>
C:\PWBproject>cd ImageAnnotator
C:\PWBproject\ImageAnnotator>cd .venv
C:\PWBproject\ImageAnnotator\.venv>cd Scripts
C:\PWBproject\ImageAnnotator\.venv\Scripts>activate.bat
----------------------------------------------

Go to ImageAnnotator folder in virtual environment:
(.venv) C:\PWBproject\ImageAnnotator>

Run file by command:
python imageAnnoAPI.py

RUN
* This code creates database 'imageAnno.db' into the same folder as the code is

RESULTS
* Created empty database 'imageAnno.db' 24 kt 

"""
# ---------------------------------------------------------------------------
# 
# check / change flask app -file location if needed
#
# check / change launch.json -file parameters and location 
# if debugging with VSC and Postman
# 
# ----------------------------------------------------------------------------
# The first time the app runs it creates the table. 
# BE CAREFULL
# With this code you can override the default table name
# ----------------------------------------------------------------------------

import flask
from flask import Flask, url_for, redirect, render_template, request, flash, send_file
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event

import os
import json
from datetime import datetime
import base64
from base64 import b64encode
# BytesIO converts data from Database into bytes
from io import BytesIO 

# create app with SQLAlchemy -----------------------------------------------------------

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
imageAnnoAPI = Flask(__name__)

imageAnnoAPI.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'imageAnno.db')
imageAnnoAPI.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(imageAnnoAPI)

# enabling foreign keys for SQLite ------------------------------------------------------

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# database models of image annotation API ------------------------------------------------

class ImageContent(db.Model):
    __tablename__ = 'imagecontent'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    data = db.Column(db.LargeBinary, nullable=False)
    ascii_data = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    location = db.Column(db.String(64))

    image_annotations = db.relationship("ImageAnnotation", back_populates="image")
    img_user = db.relationship("User", back_populates="image_user", uselist=True)
    
    def _init_(self, data, ascii_data, name, date, location):
        self.data = data
        self.ascii_data = ascii_data
        self.name = name
        self.date = date
        self.location = location
        
class ImageAnnotation(db.Model):
    __tablename__ = 'imageannotation'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey("imagecontent.id", ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    # three boolean classifiers
    meme_class = db.Column(db.Boolean, default=False, nullable=False)
    HS_class= db.Column(db.Boolean, default=False, nullable=False)
    text_class = db.Column(db.Boolean, default=False, nullable=False)
    # pos-neg polarity classifiers
    polarity_classA = db.Column(db.Integer, nullable=False)
    polarity_classB = db.Column(db.Integer, nullable=False)
    # HS classifiers
    HS_strength = db.Column(db.Integer, default=-1, nullable=False)
    HS_category = db.Column(db.String(64), nullable=False)
    # text classifiers
    text_text = db.Column(db.String(128), nullable=True)
    text_language = db.Column(db.String(32), nullable=True)

    image = db.relationship("ImageContent", back_populates="image_annotations", uselist=True)
    img_annotator = db.relationship("User", back_populates="image_annotator", uselist=True)

    def _init_(self, meme_class, HS_class, text_class, polarity_classA, polarity_classB, HS_strength, HS_category, text_text, text_language):
        self.meme_class = meme_class
        self.HS_class = HS_class
        self.text_class = text_class
        self.polarity_classA = polarity_classA
        self.polarity_classB = polarity_classB
        self.HS_strength = HS_strength
        self.HS_category = HS_category
        self.text_text = text_text
        self.text_language = text_language

# database models of photo annotation API ------------------------------------------------

class PhotoContent(db.Model):
    __tablename__ = 'photocontent'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    data = db.Column(db.LargeBinary, nullable=False)
    ascii_data = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    # date when photo was taken - don't know yet how to do
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    location = db.Column(db.String(64))

    photo_annotations = db.relationship("PhotoAnnotation", back_populates="photo")
    pho_user = db.relationship("User", back_populates="photo_user", uselist=True)
    
    def _init_(self, data, ascii_data, name, date, location):
        self.data = data
        self.ascii_data = ascii_data
        self.name = name
        self.date = date
        self.location = location
        
class PhotoAnnotation(db.Model):
    __tablename__ = 'photoannotation'

    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey("photocontent.id", ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    # boolean classifiers
    persons_class = db.Column(db.Boolean, default=False, nullable=False)
    slideshow_class = db.Column(db.Boolean, default=False, nullable=False)
    # pos value classifier
    positivity_class = db.Column(db.Integer, nullable=False)
    # text classifiers
    text_free_comment = db.Column(db.String(128), nullable=True)
    text_persons = db.Column(db.String(128), nullable=True)
    text_persons_comment = db.Column(db.String(128), nullable=True)
    # geografical location
    # not sure yet how to do

    photo = db.relationship("PhotoContent", back_populates="photo_annotations", uselist=True)
    pho_annotator = db.relationship("User", back_populates="photo_annotator", uselist=True)

    def _init_(self, persons_class, slideshow_class, positivity_class, text_free_comment, text_persons, text_persons_comment):
        self.persons_class = persons_class
        self.slideshow_class = slideshow_class
        self.positivity_class = positivity_class
        self.text_free_comment = text_free_comment
        self.text_persons = text_persons
        self.text_persons_comment = text_persons_comment

# database model for user -----------------------------------------------------------

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), nullable=False)
    user_password = db.Column(db.String(16, nullable=False))

    image_user = db.relationship("ImageContent", back_populates="img_user")
    photo_user = db.relationship("PhotoContent", back_populates="pho_user")

    image_annotator = db.relationship("ImageAnnotation", back_populates="img_annotator")
    photo_annotator = db.relationship("PhotoAnnotation", back_populates="pho_annotator")
    
    def _init_(self, user_name, user_password):
        self.user_name = user_name
        self.user_password = user_password

# -------------------------------------------------------

db.create_all()
db.session.commit()

# ------------------------------------------------------

# Render image data pictures
def data_to_ascii(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

# Upload data from folder to SQLite database for image annotation
@imageAnnoAPI.route('/uploadImage/', methods=['POST'])
def uploadImage():
    
    file = request.files.get('image', '')
        
    data = file.read()
    ascii_data = data_to_ascii(data)
    # text = request.form['text']           # ei tarvita tällä hetkellä
    location = request.form['location']

    #newFile = FileContent(name=file.filename, data=data, rendered_data=render_file, text=text, location=location)
    newFile = ImageContent(data=data, ascii_data=ascii_data, name=file.filename, date=datetime.now(), location=location)
    db.session.add(newFile)
    db.session.commit() 
    return "Database updated", 201  

# Upload data from folder to SQLite database for photo annotation
@imageAnnoAPI.route('/uploadPhoto/', methods=['POST'])
def uploadPhoto():
    
    file = request.files.get('photo', '')
        
    data = file.read()
    ascii_data = data_to_ascii(data)
    # text = request.form['text']           # ei tarvita tällä hetkellä
    location = request.form['location']

    #newFile = FileContent(name=file.filename, data=data, rendered_data=render_file, text=text, location=location)
    newFile = PhotoContent(data=data, ascii_data=ascii_data, name=file.filename, date=datetime.now(), location=location)
    db.session.add(newFile)
    db.session.commit() 
    return "Database updated", 201  

if __name__ == "__main__":    
    imageAnnoAPI.run(debug=True)