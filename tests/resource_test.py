# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# Image Annotator API database test file - db_test.py
# This file includes database test finctions of Image Annotator API.

# The file is created by example in GitHub 
# https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/db_test.py

# ----------------------------------------------

# Activate created python virtual environment (on VSC cmd):
#   cd C:\PWPproject\ImageAnnotator\.venv\Scripts
#   activate.bat

# Go to tests folder and run with command
#   (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest

# Same as above but with console output
#   (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest -s

# Run test coverage report (e.g. this)
#   (.venv) C:\PWBproject\ImageAnnotator\tests>pytest --cov-report term-missing --cov=C:/PWBproject/ImageAnnotator/hub/

#   or
#   (.venv) C:\PWBproject\ImageAnnotator\tests>pytest --cov-report term-missing --cov=C:/PWBproject/ImageAnnotator/hub/ -s 

# import python packages -----------------------------------

import glob
import json
import os
import sys
from flask.globals import request
import pytest
import tempfile
import time
import urllib.request

from datetime import datetime
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError
from werkzeug.datastructures import FileStorage

import hub
from hub import create_app, db
from hub.models import *


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    resourcetest_config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(resourcetest_config)

    #i = 0
    with app.app_context():
        db.create_all()
        #print("Numero: ", i+1)
        _populate_database()

    yield app.test_client()
    
    os.close(db_fd)
    #os.unlink(db_fname)

# ------------------------------------------------------
# Collect images and image meta data from defined ImageTest -folder to image_list

def _getImageDatas(upload):
    image_list = []
    cwd = os.getcwd()
    # get parent directory from tests = "..\\ImageAnnotator"
    parent_folder = os.path.dirname(cwd)
    folder = '\\Data\\ImageTest\\'
    source_images_folder = parent_folder + folder
    
    for filename in glob.glob(source_images_folder + '*.jpg'):
        
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

# -------------------------------------------------------------------------------
# Collect photos and photo meta data from defined PhotoTest -folder to photo_list

# from PIL import Image, ExifTags

def _getPhotoDatas(upload):
    photo_list = []
    cwd = os.getcwd()
    # get parent directory from tests = "..\\ImageAnnotator"
    parent_folder = os.path.dirname(cwd)
    folder = '\\Data\\PhotoTest\\'
    source_photos_folder = parent_folder + folder
    
    # NOTE!!! remember to set photo location, this is done differently in tests (test image folder -> static/photos)
    # in development state image is saved from request (request.image -> static/photos)

    for filename in glob.glob(source_photos_folder + '*.jpg'):
        meta_data_dict = set_photo_meta_data_to_dict(filename, True)
        meta_data_dict["location"] = hub.models.save_to_upload(upload, source_photos_folder, os.path.basename(filename))
        photo_list.append(meta_data_dict)
    return photo_list

# -----------------------------------------------------------
# CREATE AND POPULATE DATABASE

def _populate_database():
    
    # create folder images to hub static folder - images folder is created if it does not exist
    # utilizes function in models.py
    (upload_images_folder, upload_photos_folder) = create_static_folders()

    # Create new row for new user to database by using User -model
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
    userqueried = User.query.filter_by(user_name="Matti Meikäläinen").first()

    image_list = _getImageDatas(upload_images_folder)  

    for im in image_list:
        image = ImageContent(name=im["name"], 
                            publish_date=im["publish_date"], 
                            location=im["location"], 
                            is_private=False, 
                            date=im["date"])
        userqueried.image_user.append(image)
        db.session.commit()

    # collect query for defined user_name and image name
    current_user = User.query.filter_by(user_name="Matti Meikäläinen").first()
    imagename_queried = ImageContent.query.filter_by(name="kuha meemi1.jpg").first()
    
    # and commit both to database
    anno_list = hub.models.getImageAnnoData()
    for anno in anno_list:  
        annotation = ImageAnnotation(meme_class=anno["meme_class"], 
                                    HS_class=anno["HS_class"], 
                                    text_class=anno["text_class"], 
                                    polarity_classA=anno["polarity_classA"], 
                                    polarity_classB=anno["polarity_classB"], 
                                    HS_strength=anno["HS_strength"],
                                    HS_category=anno["HS_category"],
                                    text_text=anno["text_text"],
                                    text_language=anno["text_language"]) 
        current_user.image_annotator.append(annotation)
        imagename_queried.image_annotations.append(annotation)
        db.session.commit()
    
    # Collect defined user from database
    userqueried = User.query.filter_by(user_name="Meria Developer").first()

    # Add photos of photo_list for defined user in database and commit to database
    photo_list = _getPhotoDatas(upload_photos_folder) 

    for im in photo_list:
        photo = ImageContent(name=im["name"], 
                            publish_date=im["publish_date"], 
                            location=im["location"], 
                            is_private=True, 
                            date=im["date"])
        userqueried.photo_user.append(photo)
        db.session.commit()

    # collect queries for defined user_name and photo name
    current_user = User.query.filter_by(user_name="Meria Developer").first()
    photoname_queried = ImageContent.query.filter_by(name="Norja 2020.jpg").first()
    
    # and commit both to database
    anno_list = hub.models.getPhotoAnnoData()
    for anno in anno_list:
        annotation = PhotoAnnotation(persons_class=anno["persons_class"],
                                    text_persons=anno["text_persons"], 
                                    text_persons_comment=anno["text_persons_comment"], 
                                    text_free_comment=anno["text_free_comment"], 
                                    positivity_class=anno["positivity_class"], 
                                    slideshow_class=anno["slideshow_class"])   
        current_user.photo_annotator.append(annotation)
        photoname_queried.photo_annotations.append(annotation)
        db.session.commit()

# -----------------------------------------------------------
# json helper functions

def _get_user_json():
    """
    Creates a valid user JSON object to be used for PUT and POST tests.
    """
    return{
        "user_name": "Tester 123",
        "user_password": "Nhyfi875"
    }

def _get_user_json_validUser():
    return{
        "user_name": "Meria Developer",
        "user_password": "mötkäle"
    }

def _get_user_json_newPassword():
    """
    Creates a valid user JSON object to be used for PUT and POST tests.
    """
    return{
        "user_name": "Meria Developer",
        "user_password": "kukka123"
    }

def _get_user_json_newUser():
    """
    Creates a valid user JSON object to be used for PUT and POST tests.
    """
    return{
        "user_name": "New Tester",
        "user_password": "test1234"
    }      

def _get_image_json():
    # according to helpful tip from stackoverflow
    # https://stackoverflow.com/questions/35684436/testing-file-uploads-in-flask
    # for testing purposis
    # create a dummy file called test.jpg and fill it with content (in binary) abcdef
    request = {
        "user_name": "Matti Meikäläinen",
        "is_private": False
    }
    content = {
        'request': json.dumps(request),        
        'image': (BytesIO(b"abcdef"), 'test.jpg')
    }
    return content


def _get_image_json_nofilevalue():
    request = {
        "user_name": "Matti Meikäläinen",
        "is_private": False
    }
    content = {
        'request': json.dumps(request),        
        'image': ""
    }
    return content


def _get_image_json_nofileitem():
    request = {
        "user_name": "Matti Meikäläinen",
        "is_private": False
    }
    content = {
        'request': json.dumps(request)
    }
    return content


def _get_imageannotation_json():
    return  {
        "image_id": 5,
        "user_id": 3,
        "meme_class": True,
        "HS_class": False,
        "text_class": True,
        "polarity_classA": 3,
        "polarity_classB": -3,
        "HS_strength": -1,
        "HS_category": "joke",
        "text_text": "Tähän jotain suomenkielistä tekstiä ;-)))) !!",
        "text_language": "finnish"
    }

def _get_imageannotation_json_newAnno():
    return  {
        "id": 1,
        "image_id": 5,
        "user_id": 3,
        "meme_class": True,
        "HS_class": True,
        "text_class": True,
        "polarity_classA": 2,
        "polarity_classB": -2,
        "HS_strength": -2,
        "HS_category": "bully",
        "text_text": "lisää tekstiä",
        "text_language": "finnish"
    }

def _get_photo_json():
    # according to helpful tip from stackoverflow
    # https://stackoverflow.com/questions/35684436/testing-file-uploads-in-flask
    # for testing purposis
    # create a dummy file called test.jpg and fill it with content (in binary) abcdef
    request = {
        "user_name": "Meria Developer",
        "is_private": True
    }
    content = {
        'request': json.dumps(request),        
        'image': (BytesIO(b"hijklm"), 'test.jpg')
    }
    return content

def _get_photoannotation_json():
    # Creates a valid photoannotation JSON object to be used for PUT and POST tests.
    return  {	        
        "photo_id": 3,
        "user_id": 1,
        "persons_class": True,
        "slideshow_class": True,
        "positivity_class": 4,
        "text_free_comment": "Norway on summer 2020",
        "text_persons": "norwegian sheep",
        "text_persons_comment": "Norwegian sheep having a nap on shore"
    }

# -------------------------------------------------------------------------------------
# helper functions for methods

def _check_namespace(client, response):
    """
    Checks that the "annometa" namespace is found from the response body, and
    that its "name" attribute is a URL that can be accessed.
    """
    ns_href = response["@namespaces"]["annometa"]["name"]
    resp = client.get(ns_href)
    assert resp.status_code == 200
    
def _check_control_get_method(ctrl, client, obj):
    """
    Checks a GET type control from a JSON object be it root document or an item
    in a collection. Also checks that the URL of the control can be accessed.
    """
    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200

def _check_control_delete_method(ctrl, client, obj):
    """
    Checks a DELETE type control from a JSON object be it root document or an
    item in a collection. Checks the contrl's method in addition to its "href".
    Also checks that using the control results in the correct status code of 204.
    """
    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204
    
def _check_control_post_method_forUser(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid user against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_user_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_put_method_forUser(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid user against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_user_json()
    body["user_name"] = obj["user_name"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204

def _check_control_post_method_forImage(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid image against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201 (created).
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_image_json()    
    resp = client.post(href, data=body, content_type="multipart/form-data")    
    assert resp.status_code == 201

def _check_control_post_method_forImageAnnotation(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid image annotation against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201 (created).
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_imageannotation_json()    
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_put_method_forImageAnnotation(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid annotation against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_imageannotation_json_newAnno()
    body["id"] = obj["id"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204

# ---------------------------------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------------------------------

# test User Item, User Login and User Collection Resources

class TestUserCollection(object):

    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method_forUser("annometa:add-user", client, body)
        
        # 6 users populated to database
        assert len(body["items"]) == 6  
        
        for item in body["items"]:
            _check_control_get_method("self", client, item)
            _check_control_get_method("profile", client, item)

    def test_add_post(self, client):
        
        valid = _get_user_json()
        
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201        
        
        # change the received URL string into normal string for assert (i.e. Tester%20123 -> Tester 123)
        location = urllib.request.unquote(resp.headers["Location"])
        assert location.endswith(self.RESOURCE_URL + valid["user_name"] + "/")
        
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        
        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # remove model field for 400
        valid.pop("user_password")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

class TestUserLogin(object):

    RESOURCE_URL = "/api/userlogin/"

    def test_login_post(self, client):
        
        valid = _get_user_json_validUser()

        # test login with valid user_name and user_password
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 200
        
        # test with wrong content/media type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # remove model field for 400 invalid json
        valid.pop("user_password")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # unknown user_name
        valid = _get_user_json_newUser()
        # test login with unknown user_name and user_password
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 404

        # invalid user_password
        valid = _get_user_json_newPassword()
        # test login with invalid user_password
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 401

class TestUserItem(object):

    RESOURCE_URL = "/api/users/Meria%20Developer/"
    VALID_RESOURCE_URL = "/api/users/Meria Developer/"
    INVALID_URL_1 = "/api/users/invalid tester/"
    INVALID_URL_2 = "/api/users/invalid-tester/"
    
    def test_get(self, client):

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("collection", client, body)
        _check_control_put_method_forUser("edit", client, body)
        _check_control_delete_method("annometa:delete", client, body)
        
        resp = client.get(self.INVALID_URL_1)
        assert resp.status_code == 404

    def test_put(self, client):

        valid = _get_user_json()
        
        # test of wrong content type, not json, try data content instead of json        
        resp = client.put(self.VALID_RESOURCE_URL, data=valid)
        assert resp.status_code == 415

        # test of invalid url
        resp = client.put(self.INVALID_URL_1, json=valid)
        assert resp.status_code == 404

        # test of invalid url
        resp = client.put(self.INVALID_URL_2, json=valid)
        assert resp.status_code == 404

        valid = _get_user_json_newPassword()

        # test with valid user_name, do not change user_name, but change password
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        # <Response streamed [204 NO CONTENT]>

        # test with valid user name, do not change user_name, but change password
        valid["user_password"] = "newPassWord123"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        # <Response streamed [204 NO CONTENT]>

        # test 400 with defined username and undefined password field
        # user6 : (user_name = "Jussi Engineer", user_password="vl75dJrVh90765d")
        # remove password field for 400
        valid.pop("user_password")        
        resp = client.put("/api/users/Jussi%20Engineer/", json=valid)
        assert resp.status_code == 400
        # <Response streamed [400 BAD REQUEST]>

    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL_1)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL_2)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------------------------
# IMAGES
# ---------------------------------------------------------------------------------------------

# test Image and Image Collection Resources

class TestImageCollection(object):

    RESOURCE_URL = "/api/images/"

    def test_get(self, client):

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method_forImage("annometa:add-image", client, body)

        assert len(body["items"]) > 0 and len(body["items"]) == 5
        for item in body["items"]:
            assert "id" in item
            assert "user_id" in item
            assert "name" in item
            assert "publish_date" in item
            assert "location" in item
            assert "is_private" in item
            assert "date" in item

    
    def test_post(self, client):
        
        # Tests the POST method. Checks all of the possible error codes, 
        # and also checks that a valid request receives a 201 response with a location header 
        # that leads into the newly created resource.
        
        body = _get_image_json()
        
        # test with valid and see that it exists
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        #print("\n # LOCATION of image post: ", resp.headers["Location"])
        assert resp.status_code == 201

        # test correct location and url
        data_dict = json.loads(client.get(self.RESOURCE_URL).data)
        id = data_dict["items"][-1]["id"]
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + str(id) + "/")
        
        # test correct location with get
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        
        # test with wrong content type (data must be a dictionary with json part and binary part)
        resp = client.post(self.RESOURCE_URL, data=body, content_type="application/json")
        assert resp.status_code == 400
        
        body = _get_image_json()

        # remove user_name of request for 400
        req_str = body["request"]
        req_dict = json.loads(req_str)
        # remove user_name field
        req_dict = {'user_name': '', 'is_private': False}
        body["request"] = json.dumps(req_dict) 
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        assert resp.status_code == 400

        body = _get_image_json()

        # remove user name field of request for 400
        req_string = body["request"]
        # remove user_name field with pop - req_string = {"is_private": false}
        req_dicts = json.loads(req_string)
        req_dicts.pop("user_name")
        body["request"] = json.dumps(req_dicts)
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        assert resp.status_code == 400
        
        body = _get_image_json()

        # remove 'is_private' flag of request for 400
        req_string = body["request"]
        req_dicts = json.loads(req_string)
        # remove is_private field with pop 
        req_dicts.pop("is_private")
        body["request"] = json.dumps(req_dicts)
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        assert resp.status_code == 400
        
        # remove image file value of request content for 400 (no file exeption)
        body = _get_image_json_nofilevalue()
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        assert resp.status_code == 400
        
        # remove image file item of request content for 400 (no file exeption)
        body = _get_image_json_nofileitem()
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        assert resp.status_code == 400

        #print("\n -- # -- print class TestImage - RESOURCE_URL:  ", resp)
        #print("\n -- # -- print class TestImage - resp.status_code:  ", resp.status_code)

# ---------------------------------------------------------------------------------------------

# test Image and Image Item Resources
       
class TestImageItem(object):
    
    RESOURCE_URL_3 = "/api/images/3/"
    RESOURCE_URL_4 = "/api/images/4/"
    INVALID_URL = "/api/images/x/"
    UNKNOWN_URL = "/api/images/30/"
    
    def test_get(self, client):
        
        # Tests the GET method. 
        # Checks that the response status code is 200, 
        # and then checks that all of the expected attributes and controls are present, 
        # and the controls work. 
        # Checks that all items of database populuation are present, 
        # and checks that all their controls are present.

        # images/3/ --- kuha meemi3.jpg 
        
        resp = client.get(self.RESOURCE_URL_3)
        #print("\n --- image item get RESP:  ", resp)
        #print("\n --- image item get RESP status_code:  ", resp.status_code)
        assert resp.status_code == 200

        body = json.loads(resp.data)
        #print("\n --- image item get body:", body)

        assert body["id"] == 3
        assert body["user_id"] == 3
        assert body["name"] == 'kuha meemi3.jpg'
        assert body["publish_date"] == '2021-04-19 10:53:28'
        assert "\\static\\images\\" in body["location"]
        assert body["is_private"] == False
        
        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("collection", client, body)
        _check_control_delete_method("annometa:delete", client, body)
        #_check_control_edit_image_item("edit", client, body) ----------- EI TOIMI --------

        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

        resp = client.get(self.UNKNOWN_URL)
        assert resp.status_code == 404


    def test_put(self, client):
        
        # Tests the PUT method. 
        # Checks all of the possible error codes, 
        # and also checks that a valid request receives a 204 response. 
        # Also tests that when name is changed, the photo can be found from a its new URI. 
        
        request = {
            "name": "newName.jpg"
        }
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL_3, data=json.dumps(request))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=request)
        assert resp.status_code == 404
        
        # test with another image's name
        duplicate_request = {
            "name": "kuha meemi1.jpg"
        }
        
        resp = client.put(self.RESOURCE_URL_4, json=duplicate_request)
        assert resp.status_code == 409
        
        # test with valid (only change id)
        
        resp = client.put(self.RESOURCE_URL_3, json=request)
        assert resp.status_code == 204
        
        # remove field for 400
        # try to name to the same as itself and the recently added 
        resp = client.put(self.RESOURCE_URL_3, json=request)
        assert resp.status_code == 409

        empty_name_request = {
            "name": ""
        }
        resp = client.put(self.RESOURCE_URL_3, json=empty_name_request)
        assert resp.status_code == 400
        
        empty_name_request = {
            "" : ""
        }
        resp = client.put(self.RESOURCE_URL_3, json=empty_name_request)
        assert resp.status_code == 400


    def test_delete(self, client):
        
        # Tests the DELETE method. 
        # Checks that a valid request reveives 204 response, 
        # and that trying to GET the photo afterwards results in 404.
        # Also checks that trying to delete a photo that doesn't exist results in 404.
        
        resp = client.delete(self.RESOURCE_URL_3)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL_3)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
        resp = client.delete(self.UNKNOWN_URL)
        assert resp.status_code == 404

# ---------------------------------------------------------------------------------------------

# test Imageannotation and Imageannotation Collection Resources

class TestImageannotationCollection(object):

    RESOURCE_URL = "/api/imageannotations/"

    def test_get(self, client):
        
        resp = client.get(self.RESOURCE_URL)
        #print("\n -- # -- get ImageannotationCollection - RESOURCE_URL:  ", resp)
        #print("\n -- # -- get ImageannotationCollection - resp.status_code:  ", resp.status_code)
        assert resp.status_code == 200
        
        body = json.loads(resp.data)
        #print("\n -- # -- get ImageannotationCollection - BODY:  ", body)
        _check_namespace(client, body)

        _check_control_post_method_forImageAnnotation("annometa:add-imageannotation", client, body)

        # only 1 photoannotation in database
        assert len(body["items"]) > 0 and len(body["items"]) == 1
    
        for item in body["items"]:
            assert "image_id" in item
            assert "user_id" in item
            assert "meme_class" in item
            assert "HS_class" in item
            assert "text_class" in item
            assert "polarity_classA" in item
            assert "polarity_classB" in item
            assert "HS_strength" in item
            assert "HS_category" in item
            assert "text_text" in item
            assert "text_language" in item

    def test_post(self, client):
        
        # Tests the POST method. Checks all of the possible error codes, 
        # and also checks that a valid request receives a 201 response with a location header 
        # that leads into the newly created resource.
        
        body = _get_imageannotation_json()
        #print("\n -- # -- post ImageannotationCollection - BODY:  ", body)
        
        # test with valid and see that it exists
        resp = client.post(self.RESOURCE_URL, data=json.dumps(body), content_type="application/json")
        assert resp.status_code == 201
        
        # test correct location and url
        data_dict = json.loads(client.get(self.RESOURCE_URL).data)
        id = data_dict["items"][-1]["id"]
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + str(id) + "/")
        
        # test correct location with get
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        
        # test with wrong content type (data must be a dictionary with json part and binary part)
        resp = client.post(self.RESOURCE_URL, data=body, content_type="application/json")
        assert resp.status_code == 400

        valid = _get_imageannotation_json()

        # remove model user_id field for 400
        valid.pop("user_id")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        valid = _get_imageannotation_json()

        # remove model image_id field for 400
        valid.pop("image_id")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        body = _get_imageannotation_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        assert resp.status_code == 415


# ---------------------------------------------------------------------------------------------

# test Imageannotation and Imageannotation Item Resources
       
class TestImageannotationItem(object):
    
    RESOURCE_URL = "/api/imageannotations/1/"
    RESOURCE_URL_2 = "/api/imageannotations/2/"
    INVALID_URL = "/api/imageannotations/x/"
    UNKNOWN_URL = "/api/imageannotations/30/"
    
    def test_get(self, client):

        # /api/imageannotations/1/ --- "kuha meemi1.jpg"

        #body = _get_imageannotation_json()
        
        resp = client.get(self.RESOURCE_URL)
        print("\n -- # -- imageannotation get - RESOURCE_URL:  ", resp)
        print("\n -- # -- imageannotation get - resp.status_code:  ", resp.status_code)
        assert resp.status_code == 200

        body = json.loads(resp.data)
        print("\n --- image annotation get body:", body)

        assert body["id"] == 1
        assert body["image_id"] == 2
        assert body["user_id"] == 3
        assert body["meme_class"] == True
        assert body["HS_class"] == False
        assert body["text_class"] == True
        assert body["polarity_classA"] == -1
        assert body["polarity_classB"] == -3
        assert body["HS_strength"] == -2
        assert body["HS_category"] == 'bully'
        assert body["text_text"] == 'Tähän jotain suomenkielistä tekstiä ;-)))) !!'
        assert body["text_language"] == 'finnish'

        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("collection", client, body)
        _check_control_delete_method("annometa:delete", client, body)
        #_check_control_put_method_forImageAnnotation("edit", client, body)

        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

        resp = client.get(self.UNKNOWN_URL)
        assert resp.status_code == 404


    def test_put(self, client):
        
        # Tests the PUT method. 
        # Checks all of the possible error codes, 
        # and also checks that a valid request receives a 204 response. 
        # Also tests that when id is changed, the annotation can be found from a its new URI. 
        
        request = _get_imageannotation_json()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(request))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=request)
        assert resp.status_code == 404

        # test with valid (do not change annotation id)
        resp = client.put(self.RESOURCE_URL, json=request)
        assert resp.status_code == 204


    def test_delete(self, client):
        
        # Tests the DELETE method. 
        # Checks that a valid request reveives 204 response, 
        # and that trying to GET the annotation afterwards results in 404.
        # Also checks that trying to delete annotation that doesn't exist results in 404.
        
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
        resp = client.delete(self.UNKNOWN_URL)
        assert resp.status_code == 404
