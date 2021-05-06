# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# Image Annotator API database test file - db_test.py
# This file includes database test finctions of Image Annotator API.

# The file is created by example in GitHub 
# https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/db_test.py

"""
# ----------------------------------------------

Activate created python virtual environment (on VSC cmd):
cd C:\PWBproject\ImageAnnotator\.venv\Scripts
activate.bat

# ---- OR

C:\PWBproject>
C:\PWBproject>cd ImageAnnotator
C:\PWBproject\ImageAnnotator>cd .venv
C:\PWBproject\ImageAnnotator\.venv>cd Scripts
C:\PWBproject\ImageAnnotator\.venv\Scripts>activate.bat

# ----------------------------------------------

Set cofiguration setting class as 'development' or 'production' or 'default'
    (.venv) C:\PWBproject\ImageAnnotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\PWBproject\ImageAnnotator\extracodes>set FLASK_APP=hub

"""

# run with command
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest
# same as above but with console output
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest -s 

# import python packages -----------------------------------

import json
import time
from datetime import datetime
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

import os
import pytest
import tempfile

import base64
from io import BytesIO

# import hub (image annotator) ------------------------------

import hub
from hub import create_app, db
from hub.models import User, ImageContent, ImageAnnotation, PhotoAnnotation

# -----------------------------------------------------------

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# -----------------------------------------------------------
# creates temporary database handle only for testing purposes

@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()

    dbtest_config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    app = create_app(dbtest_config)

    with app.app_context():
        db.create_all()

    yield app
    
    #app.db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)

# -----------------------------------------------------------

def _get_image():
    cwd = os.getcwd()   # get current working directory
    folder = '\\tests\\'
    location = cwd + folder
    imagefilename = 'kuha meemi1.jpg'
    path_to_file = location + imagefilename
    #print("Current working directory: {0}".format(cwd))
    print("get_image path: ", path_to_file)
    with open(location + imagefilename, "rb") as f:
        #image_binary = f.read()
        #image_ascii = base64.b64encode(image_binary).decode('ascii')
        timestamp = os.path.getctime(path_to_file)  # get created time
        datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print("datetime:", datetime_str)
        
        # Note! publish_date = creation date ; date = datetime now
        image_dict = {
            #"image_data": image_binary,
            #"image_ascii": image_ascii,
            "name": imagefilename,
            "publish_date": datetime.fromisoformat(datetime_str),
            "location": location,
            "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        return image_dict

def _get_user():
    user = User(user_name = "testaaja", user_password="mfir7ihf9w8")
    return user

def _get_image_content(received_is_private):
    test_image = _get_image()
    return ImageContent(
        #data=test_image["image_data"],
        #ascii_data=test_image["image_ascii"],
        name=test_image["name"],
        publish_date=test_image["publish_date"],
        location=test_image["location"],
        is_private=received_is_private,
        date=datetime.now()
    )

def _get_image_annotation():
    return ImageAnnotation(
        meme_class=True,
        HS_class=True,
        text_class=True,
        polarity_classA=1, 
        polarity_classB=2,
        HS_strength=-1,
        HS_category="some category",
        text_text="text here",
        text_language="Finnish"
    )

def _get_photo_annotation():
    return PhotoAnnotation(
        persons_class = False,
        slideshow_class = False,
        positivity_class = 2,
        text_free_comment = "Beach is beautiful",
        text_persons = "Text here",
        text_persons_comment = "Comment here",
    )

# --------------------------------------------------------------

def test_create_model_instances(app):
    """
    Tests that we can create one instance of each model, 
    and save them to the database using valid values for all columns. 
    After creation, test that everything can be found from database, 
    and that all relationships have been saved correctly.
    """
    # Create everything
    
    # add user
    with app.app_context():
        user = _get_user()
        db.session.add(user)
        db.session.commit()

        # query user from database
        queryUser = User.query.filter_by(id=1).first()
        
        # add image for user
        image = _get_image_content(False)
        queryUser.image_user.append(image)
        db.session.commit()

        # add annotation for user and image
        newImage = ImageContent.query.filter_by(id=1).first()
        image_annotation = _get_image_annotation()
        queryUser.image_annotator.append(image_annotation)
        newImage.image_annotations.append(image_annotation)
        db.session.commit()
        
        # add photo for user
        photo = _get_image_content(True)
        queryUser.photo_user.append(photo)
        db.session.commit()

        # add annotation for user and photo
        newPhoto = ImageContent.query.filter_by(id=2).first()
        photo_annotation = _get_photo_annotation()
        queryUser.photo_annotator.append(photo_annotation)
        newPhoto.photo_annotations.append(photo_annotation)
        db.session.commit()

        # Check that everything exists --------------------
        assert User.query.count() == 1
        assert ImageContent.query.count() == 2
        assert ImageAnnotation.query.count() == 1        
        assert PhotoAnnotation.query.count() == 1

        db_user = User.query.first()
        db_imagecontent = ImageContent.query.first()
        db_imageannotation = ImageAnnotation.query.first()
        db_photoannotation = PhotoAnnotation.query.first()

        # Check all relationships --------------------------
        # Check all relationships (both sides)
        # image
        db_imagecontent1 = ImageContent.query.filter_by(id=1).first()
        # photo
        db_imagecontent2 = ImageContent.query.filter_by(id=2).first()

        print("imagecontent1_user:", db_imagecontent1.image_users)
        print("imagecontent1_user:", db_user)
        assert db_imagecontent1.image_users[0] == db_user

        print("imagecontent1", db_imageannotation.images)
        print("imagecontent1", db_imagecontent1)
        assert db_imageannotation.images[0] == db_imagecontent1

        print("imagecontent2_user:", db_imagecontent2.photo_users)
        print("imagecontent2_user:", db_user)
        assert db_imagecontent2.photo_users[0] == db_user

        print("imagecontent2", db_photoannotation.photos)
        print("imagecontent2", db_imagecontent2)
        assert db_photoannotation.photos[0] == db_imagecontent2
        
        assert db_user.image_user[0] == db_imagecontent1
        assert db_user.photo_user[1] == db_imagecontent2

        assert db_user.image_annotator[0] == db_imageannotation
        assert db_user.photo_annotator[0] == db_photoannotation

        db.session.rollback()

# ----------------------------------------------------------------------
# test database table columns

def test_user_columns(app):
    # Tests user columns' restrictions. 
    # user_name must be unique
    # user_name is mandatory

    with app.app_context():
        user_1 = _get_user()
        user_2 = _get_user()
        db.session.add(user_1)
        db.session.add(user_2)    
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()
        
        user = _get_user()
        user.user_name = None
        db.session.add(user)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

# --------------------------------------------------------------

def test_image_content_columns(app):
    # Tests image content columns' restrictions. 
    # data, ascii_data, name, location, is_private and date are mandatory fields

    with app.app_context():
        # add image to image content
        """
        image = _get_image_content(False)
        image.data = None
        db.session.add(image)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()
        """
        """
        image = _get_image_content(False)
        image.ascii_data = None
        db.session.add(image)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()
        """
        image = _get_image_content(False)
        image.name = None
        db.session.add(image)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        image = _get_image_content(False)
        image.location = None
        db.session.add(image)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # NOT! "image.date" does not give IntegrityError, if "default" is set in database
        image = _get_image_content(False)
        image.date = None
        print("image.date:", image.date)
        db.session.add(image)
        print("image", image.date)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()


def test_image_annotation_columns(app):
    # Tests image annotation columns' restrictions. 
    # meme_class, HS_class and text_class are mandatory fields

    with app.app_context():
        # add image to image content
        
        imageAnno = _get_image_annotation()
        imageAnno.meme_class = None
        db.session.add(imageAnno)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        imageAnno = _get_image_annotation()
        imageAnno.HS_class = None
        db.session.add(imageAnno)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        imageAnno = _get_image_annotation()
        imageAnno.text_class = None
        db.session.add(imageAnno)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # TAMAN VOI POISTAA SILLA ON NOLLATTAVA MUUTTUJA
        #imageAnno = _get_image_annotation()
        #imageAnno.polarity_classA = None
        #db.session.add(imageAnno)
        #with pytest.raises(IntegrityError):
        #    db.session.commit()
        #db.session.rollback()

def test_photo_annotation_columns(app):
    # Tests photo annotation columns' restrictions. 
    # persons_class, slideshow_class and positivity_class are mandatory fields

    with app.app_context():
        # add annotation to photo annotation
        
        photoAnno = _get_photo_annotation()
        photoAnno.persons_class = None
        db.session.add(photoAnno)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        photoAnno = _get_photo_annotation()
        photoAnno.slideshow_class = None
        db.session.add(photoAnno)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        photoAnno = _get_photo_annotation()
        photoAnno.positivity_class = None
        db.session.add(photoAnno)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


# test delete ------------------------------------------------------------------------

def test_photoannotation_ondelete_photo(app):
    # Tests that photo's foreign key on photoannotation is set to null when photo is deleted.

    with app.app_context():
        
        testphoto = _get_image_content(True)
        db.session.add(testphoto)
        testphotoannotation = _get_photo_annotation()
        testphoto.photo_annotations.append(testphotoannotation)
        db.session.commit()
        db.session.delete(testphoto)
        db.session.commit()

        # NOTE! When image is removed, the annotation remains
        assert ImageContent.query.count() == 0
        assert testphotoannotation.photos == []
        assert ImageAnnotation.query.count() == 0
        assert PhotoAnnotation.query.count() == 1


def test_imageannotation_ondelete_image(app):
    # Tests that images's foreign key on imageannotation is set to null when image is deleted.

    with app.app_context():
        
        testimage = _get_image_content(False)
        db.session.add(testimage)
        testimageannotation = _get_image_annotation()
        testimage.image_annotations.append(testimageannotation)
        db.session.commit()
        db.session.delete(testimage)
        db.session.commit()

        # NOTE! When image is removed, the annotation remains
        assert ImageContent.query.count() == 0
        assert testimageannotation.images == []
        assert ImageAnnotation.query.count() == 1
        assert PhotoAnnotation.query.count() == 0


def test_photo_and_photoannotation_ondelete_user(app):
    # Tests that users's foreign key on photoannotation is set to null when user is deleted.

    with app.app_context():
        
        testuser = _get_user()
        db.session.add(testuser)
        db.session.commit()
        # query user from database
        queryUser = User.query.filter_by(id=1).first()
        # add photo for user
        testphoto = _get_image_content(True)
        queryUser.image_user.append(testphoto)
        db.session.commit()
        testphotoannotation = _get_photo_annotation()
        testphoto.photo_annotations.append(testphotoannotation)
        db.session.commit()

        db.session.delete(testuser)
        db.session.commit()

        # NOTE! When user is removed, the image and annotation remains
        assert User.query.count() == 0
        assert testphoto.photo_users == []
        assert testphotoannotation.photo_annotators == []
        assert ImageContent.query.count() == 1
        assert PhotoAnnotation.query.count() == 1
        assert ImageAnnotation.query.count() == 0




"""
# THIS CANNOT BE TESTED ??? ------------------------------------------------------------

# should test relationship between three tables: user - image - annotation

def test_imagecontent_imageannotation_one_to_one(app):
    
    # Tests that the relationship between image content and image annotation is one-to-one.
    # User can give only one annotation for image.
    # For example user cannot assign two different annotations for one image.
    
    with app.app_context():

        # Create everything that is needed for test
        
        # add user
        user = _get_user()
        db.session.add(user)
        db.session.commit() # JUHA POISTI KOMMENTIN
        # query user from database
        newUser = User.query.filter_by(id=1).first()
        print("newUser", newUser.user_name)
        
        # add image for user
        image = _get_image_content(False)
        newUser.image_user.append(image)
        db.session.commit()    # JUHA POISTI KOMMENTIN
        # query image from database # JUHA MUUTTI KOMENTIB ## add annotation for user and image
        newImage = ImageContent.query.filter_by(id=1).first()
        print("newImage", newImage.name)

        # create annotation 1
        image_annotation1 = _get_image_annotation()
        newUser.image_annotator.append(image_annotation1)
        newImage.image_annotations.append(image_annotation1)
        db.session.commit() # JUHA
        print("image_annotation1", image_annotation1.text_text)

        # create annotation 2
        image_annotation2 = _get_image_annotation()
        newUser.image_annotator.append(image_annotation2)
        print("image_annotation2", image_annotation2.text_text)
        #print("user.image.image_annotation2", newUser.image_user.image_annotator.text_text)
        newImage.image_annotations.append(image_annotation2)
        print("newImage", newImage.image_annotations )
        #db.session.commit()  # JUHA

        # testing
        #image_1 = _get_image_content(1)
        #image_2 = _get_image_content(2)
        #image_1.annotation = annotation
        #image_2.annotation = locatioannotation
        
        #db.session.add(image)
        #db.session.add(image_annotation1)
        #db.session.add(image_annotation2)    
        with pytest.raises(IntegrityError):
            db.session.commit()
"""