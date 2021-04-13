# database test
# kuten github -esimerkissä
# https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/db_test.py

# run with command
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest
# same as above but with console output
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest -s 

import os
import pytest
import tempfile
from datetime import datetime
import base64
from io import BytesIO

import hub
from hub import create_app, db
from hub.models import User, ImageAnnotation, ImageContent, PhotoAnnotation

@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()    
    
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
    yield app
    
    os.close(db_fd)
    os.unlink(db_fname)


def _get_image():
    location = "C:\\PWBproject\\ImageAnnotator\\tests\\"
    name = 'kuha meemi1.jpg'
    with open(location + name, "rb") as f:
        image_binary = f.read()
        image_ascii = base64.b64encode(image_binary).decode('ascii')
        image_dict = {
            "image_data":image_binary,
            "image_ascii":image_ascii,
            "name":name,
            "publish_date":publish_date,
            "location":location
        }
        return image_dict

def _get_photo():
    location = 'C:\\PWBproject\\ImageAnnotator\\tests\\'
    name = 'Norja 2020.jpg'
    with open(location + name, "rb") as f:
        image_binary = f.read()
        image_ascii = base64.b64encode(image_binary).decode('ascii')
        image_dict = {
            "image_data":image_binary,
            "image_ascii":image_ascii,
            "name":name,
            "publish_date":publish_date,
            "location":location
        }
        return photo_dict

def _get_user():
    user = User(user_name = "testaaja", user_password="mfir7ihf9w8")
    return user

def _get_image_content(received_is_private):
    test_image = _get_image()
    return ImageContent(
        data=test_image["image_data"],
        ascii_data=test_image["image_ascii"],
        name=test_image["name"],
        publish_date=test_image["publish_date"],
        location=test_image["location"],
        is_private=received_is_private
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

def _get_photo_content():
    test_photo = _get_photo()
    return PhotoContent(
        data=test_photo["image_data"],
        ascii_data=test_photo["image_ascii"],
        name=test_photo["name"],
        publish_date=test_photo["publish_date"],
        location=test_photo["location"],
        is_private=received_is_not_private
        date=datetime.now()
    )

def _get_photo_annotation():
    return PhotoAnnotation(
        persons_class = False,
        slideshow_class = False,
        positivity_class = 2,
        text_free_comment = "Beach",
        text_persons = "Text here",
        text_persons_comment = "Comment here",
    )

def test_create_model_instances(app):
    """
    Tests that we can create one instance of each model and save them to the
    database using valid values for all columns. After creation, test that 
    everything can be found from database, and that all relationships have been
    saved correctly.
    """
    
    with app.app_context():
        # Create everything
        user = _get_user()
        db.session.add(user)
        db.session.commit()
        #
        newUser = User.query.filter_by(id=1).first()
        image = _get_image_content(False)
        newUser.image_user.append(image)
        db.session.commit()
        #
        newImage = ImageContent.query.filter_by(id=1).first()
        image_annotation = _get_image_annotation()
        newUser.image_annotator.append(image_annotation)
        newImage.image_annotations.append(image_annotation)
        db.session.commit()
        #
        photo = _get_image_content(True)
        #newUser.photo_user.append(photo)
        newUser.image_user.append(photo)
        db.session.commit()

        #newPhoto = PhotoContent.query.filter_by(id=1).first()
        newPhoto = ImageContent.query.filter_by(id=2).first()

        photo_annotation = _get_photo_annotation()
        newUser.photo_annotator.append(photo_annotation)
        newPhoto.photo_annotations.append(photo_annotation)
        db.session.commit()

        # Check that everything exists --------------------
        assert User.query.count() == 1
        assert ImageContent.query.count() == 1
        assert ImageAnnotation.query.count() == 1
        assert PhotoContent.query.count() == 1
        assert PhotoAnnotation.query.count() == 1

        db_user = User.query.first()
        db_imagecontent = ImageContent.query.first()
        db_imageannotation = ImageAnnotation.query.first()
        #db_photocontent = PhotoContent.query.first()
        db_photocontent = ImageContent.query.first()
        db_photoannotation = PhotoAnnotation.query.first()

        # Check all relationships --------------------------
        # Check all relationships (both sides)

        print(db_imagecontent.img_user)
        print(db_user)
        assert db_imagecontent.img_user[0] == db_user

        print(db_imageannotation.image)
        print(db_imagecontent)
        assert db_imageannotation.image[0] == db_imagecontent
        
        # TEE MYÖS LOPUT VERTAILUT kaikille suhteille
        