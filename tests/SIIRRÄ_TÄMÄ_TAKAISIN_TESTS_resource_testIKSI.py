# resource test
# created according to example in github:
#   https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/db_test.py

# run with command
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest
# same as above but with console output
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest -s 

# import python packages ------------------------------

import os
import pytest
import tempfile
import json
import time
from datetime import datetime
import base64
from io import BytesIO
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

# import api files and functions -----------------------

#from app import create_app, db
#import app
from hub import create_app, db
from hub.models import User, ImageContent, ImageAnnotation, PhotoAnnotation

# ------------------------------------------------------
# define and use testing confuguration
# based on http://flask.pocoo.org/docs/1.0/testing/
# client is not neeeded for database and resources testing
# db handle is needed for db and resource testing

@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()    
    
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        
    yield app

    os.close(db_fd)
    os.unlink(db_fname)

# ------------------------------------------------------
# CREATE AND POPULATE DATABASE

def _get_image():
    location = "C:\\PWBproject\\ImageAnnotator\\tests\\"
    name = 'kuha meemi1.jpg'
    with open(location + name, "rb") as f:
        image_binary = f.read()
        image_ascii = base64.b64encode(image_binary).decode('ascii')
        image_dict = {
            "image_data":image_binary,
            "image_ascii":image_ascii,
            "location":location,
            "name":name
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
            "location":location,
            "name":name
        }
        return image_dict

def _get_user():
    user = User(user_name = "testaaja", user_password="mfir7ihf9w8")
    return user

def _get_image_content():
    test_image = _get_image()
    return ImageContent(
        name=test_image["name"],
        data=test_image["image_data"],
        ascii_data=test_image["image_ascii"],
        date=datetime.now(),
        location=test_image["location"]
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
    test_image = _get_photo()
    return PhotoContent(
        name=test_image["name"],
        data=test_image["image_data"],
        ascii_data=test_image["image_ascii"],
        date=datetime.now(),
        location=test_image["location"]
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

def create_and_populate_database(app):
    """
    # Creates and populates database for resource testing purposes.
    """
    
    with app.app_context():
        # Create everything in steps
        user = _get_user()
        db.session.add(user)
        db.session.commit()
        #
        newUser = User.query.filter_by(id=1).first()
        image = _get_image_content()
        newUser.image_user.append(image)
        db.session.commit()
        #
        newImage = ImageContent.query.filter_by(id=1).first()
        image_annotation = _get_image_annotation()
        newUser.image_annotator.append(image_annotation)
        newImage.image_annotations.append(image_annotation)
        db.session.commit()
        #
        photo = _get_photo_content()
        newUser.photo_user.append(photo)
        db.session.commit()
        #
        newPhoto = PhotoContent.query.filter_by(id=1).first()
        photo_annotation = _get_photo_annotation()
        newUser.photo_annotator.append(photo_annotation)
        newPhoto.photo_annotations.append(photo_annotation)
        db.session.commit()

# ---------------------------------------------------------
"""
def _get_sensor_json(number=1):
    
    # Creates a valid photo JSON object to be used for PUT and POST tests.
    
    return {"name": "extra-sensor-{}".format(number), "model": "extrasensor"}
"""

# namespace = annometa

def check_namespace(client, response):
    """
    # Checks that the "annometa" namespace is found from the response body, 
    # and that its "name" attribute is a URL that can be accessed.
    """
    ns_href = response["@namespaces"]["annometa"]["name"]
    resp = client.get(ns_href)
    assert resp.status_code == 200

"""
#
def _check_control_get_method(ctrl, client, obj):
    """
    # Checks a GET type control from a JSON object be it root document or an item in a collection. 
    # Also checks that the URL of the control can be accessed.
    """
    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200

#
def _check_control_delete_method(ctrl, client, obj):
    """
    # Checks a DELETE type control from a JSON object be it root document 
    # or an item in a collection. 
    # Checks the contrl's method in addition to its "href".
    # Also checks that using the control results in the correct status code of 204.
    """
    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204


# check post for user
def _check_control_post_method_user(ctrl, client, obj):
    """
    # Checks a POST type control from a JSON object be it root document or an item in a collection. 
    # In addition to checking the "href" attribute, also checks that method, 
    # encoding and schema can be found from the control. 
    # Also validates a valid sensor against the schema of the control to ensure that they match. 
    # Finally checks that using the control results in the correct status code of 201.
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


# check post for photo
def _check_control_post_method_photo(ctrl, client, obj):
    """
    # Checks a POST type control from a JSON object be it root document or an item in a collection. 
    # In addition to checking the "href" attribute, also checks that method, 
    # encoding and schema can be found from the control. 
    # Also validates a valid sensor against the schema of the control to ensure that they match. 
    # Finally checks that using the control results in the correct status code of 201.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_photo_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201


# check post for photoannotation
def _check_control_post_method_photoannotation(ctrl, client, obj):
    """
    # Checks a POST type control from a JSON object be it root document or an item in a collection. 
    # In addition to checking the "href" attribute, also checks that method, 
    # encoding and schema can be found from the control. 
    # Also validates a valid sensor against the schema of the control to ensure that they match. 
    # Finally checks that using the control results in the correct status code of 201.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_photoannotation_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201


# check put for user
def _check_control_put_method_user(ctrl, client, obj):
    """
    # Checks a PUT type control from a JSON object be it root document or an item in a collection. 
    # In addition to checking the "href" attribute, also checks that method, 
    # encoding and schema can be found from the control. 
    # Also validates a valid sensor against the schema of the control to ensure that they match. 
    # Finally checks that using the control results in the correct status code of 204.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    # for user
    body = _get_user_json()
    body["name"] = obj["name"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204


# check put for photo
def _check_control_put_method_photo(ctrl, client, obj):
    """
    # Checks a PUT type control from a JSON object be it root document or an item in a collection. 
    # In addition to checking the "href" attribute, also checks that method, 
    # encoding and schema can be found from the control. 
    # Also validates a valid sensor against the schema of the control to ensure that they match. 
    # Finally checks that using the control results in the correct status code of 204.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    # for photo
    body = _get_photo_json()
    body["id"] = obj["id"]
    
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204


# for check put photoannotation
def _check_control_put_method_photo(ctrl, client, obj):
    """
    # Checks a PUT type control from a JSON object be it root document or an item in a collection. 
    # In addition to checking the "href" attribute, also checks that method, 
    # encoding and schema can be found from the control. 
    # Also validates a valid sensor against the schema of the control to ensure that they match. 
    # Finally checks that using the control results in the correct status code of 204.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    # for photo
    body = _get_photoannotation_json()
    body["id"] = obj["id"]
    
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204


#############################################################################
# test User and User Collection 

class TestUserCollection(object):

    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        """
        # Tests the GET method. 
        # Checks that the response status code is 200, 
        # and then checks that all of the expected attributes and controls are present, 
        # and the controls work. 
        # Checks that all items of database population are present, 
        # and checks that all their controls are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method_user("annometa:add-user", client, body)
        assert len(body["items"]) == 2
        for item in body["items"]:
            assert "user_name" in item
            assert "user_password" in item

    def test_post(self, client):
        """
        # Tests the POST method. 
        # Checks all of the possible error codes, 
        # and also checks that a valid request receives a 201 response with a location header 
        # that leads into the newly created resource.
        """
        valid = _get_user_json()

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        body = json.loads(client.get(self.RESOURCE_URL).data)
        id = body["items"][-1]["name"] 
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + str(id) + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)

        ####### tarkista alla oleavat tiedot #############
        # user_name="testaaja", user_password="mfir7ihf9w8")

        assert body["user_name"] == "testaaja"
        assert body["user_password"] == "mfir7ihf9w8"

        # test with wrong content type(must be json)
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # remove title field for 400
        valid.pop("user_name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestUserItem(object):

    RESOURCE_URL = "/api/users/Meria/"
    INVALID_URL = "/api/users/3/"
    MODIFIED_URL = "/api/users/MerjaKK/"

    def test_get(self, client):
        """
        # Tests the GET method. 
        # Checks that the response status code is 200, 
        # and then checks that all of the expected attributes and controls are present, 
        # and the controls work. 
        # Checks that all items of database population are present, 
        # and chcks that all their controls are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["user_name"] == "Meria"
        assert body["user_password"] == "mfir7ihf9w8"
        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("collection", client, body)
        _check_control_put_method_user("edit", client, body)
        _check_control_delete_method("annometa:delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404


    def test_put(self, client):
        """
        # Tests the PUT method. 
        # Checks all of the possible error codes, 
        # and also checks that a valid request receives a 204 response. 
        # Also tests that when user_name is changed, the match can be found from a its new URI. 
        """
        valid = _get_user_json()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
       
        # test with another player's id
        valid["user_name"] = "Juhis"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # test with valid (only change name)
        valid["user_name"] = "Juha"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        #valid.pop("user_password")
        #resp = client.put(self.RESOURCE_URL, json=valid)
        #assert resp.status_code == 400
        
        valid = _get_user_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["user_password"] == valid["user_password"]


    def test_delete(self, client):
        """
        # Tests the DELETE method. 
        # Checks that a valid request reveives 204 response, 
        # and that trying to GET the user afterwards results in 404.
        # Also checks that trying to delete a user that doesn't exist results in 404.
        """
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404


#############################################################################
# test Photo and Photo Collection Resources

class TestPhotoCollection(object):

    RESOURCE_URL = "/api/photos/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method_photo("annometa:add-photo", client, body)
        assert len(body["items"]) == 2
        for item in body["items"]:
            assert "id" in item
            assert "user_id" in item
            assert "data" in item
            assert "ascii_data" in item
            assert "name" in item
            assert "publish_date" in item
            assert "location" in item
            assert "is_private" in item
            assert "date" in item


    def test_post(self, client):
        """
        # Tests the POST method. 
        # Checks all of the possible error codes, 
        # and also checks that a valid request receives a 201 response with a location header 
        # that leads into the newly created resource.
        """
        valid = _get_photo_json()

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        body = json.loads(client.get(self.RESOURCE_URL).data)
        id = body["items"][-1]["id"]
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + str(id) + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)

        #    mitä tähän merkitään ?       ##############################

        assert body["id"] == 3
        assert body["user_id"] == "1"
        assert body["data"] == " "
        assert body["ascii_data"] == " "
        assert body["publish_date"] == "xxx xxx"
        assert body["location"] == "xxx"
        assert body["is_private"] == "xxx xxx"
        assert body["date"] == "xxxx"

        # test with wrong content type (content must be json)
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # remove title field for 400
        valid.pop("id")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestPhotoItem(object):
    
    RESOURCE_URL = "/api/photos/1/"
    INVALID_URL = "/api/photos/x/"
    MODIFIED_URL = "/api/photos/30/"
    
    def test_get(self, client):
        """
        # Tests the GET method. 
        # Checks that the response status code is 200, 
        # and then checks that all of the expected attributes and controls are present, 
        # and the controls work. 
        # Checks that all items of database populuation are present, 
        # and checks that all their controls are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)

        #    mitä tähän merkitään ?       ##############################

        assert body["id"] == 3
        assert body["user_id"] == "1"
        assert body["data"] == " "
        assert body["ascii_data"] == " "
        assert body["publish_date"] == "xxx xxx"
        assert body["location"] == "xxx"
        assert body["is_private"] == "xxx xxx"
        assert body["date"] == "xxxx"

        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("collection", client, body)
        _check_control_put_method_photo("edit", client, body) 
        _check_control_delete_method("annometa:delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404
       
    def test_put(self, client):
        """
        # Tests the PUT method. 
        # Checks all of the possible error codes, 
        # and also checks that a valid request receives a 204 response. 
        # Also tests that when name is changed, the photo can be found from a its new URI. 
        """
        valid = _get_photo_json()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with another photo's id
        valid["id"] = 2
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # test with valid (only change id)
        valid["id"] = 1
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("lammaskuva")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        valid = _get_match_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["lammaskuva"] == valid["lammaskuva"]
               
    def test_delete(self, client):
        """
        # Tests the DELETE method. 
        # Checks that a valid request reveives 204 response, 
        # and that trying to GET the photo afterwards results in 404.
        # Also checks that trying to delete a photo that doesn't exist results in 404.
        """
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404


#############################################################################
# test Photo and Photo Collection Resources

"""