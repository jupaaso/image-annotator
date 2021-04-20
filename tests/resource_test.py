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
"""

# run with command
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest
# same as above but with console output
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest -s 

# import python packages -----------------------------------

import json
import os
import pytest
import tempfile
import time

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

    with app.app_context():
        db.create_all()
        _populate_database()

    yield app.test_client()
    
    os.close(db_fd)
    os.unlink(db_fname)

# ------------------------------------------------------
# CREATE AND POPULATE DATABASE

def _populate_database():
# Create new row for new user to database by using User -model
    user1 = User(user_name = "Meria Developer", user_password="mötkäle")
    user2 = User(user_name = "Juhis Engineer", user_password="auty8f645bf")
    user3 = User(user_name = "Matti Meikäläinen", user_password="1234567890")
    user4 = User(user_name = "Katti ole' Matikainen", user_password="åäöpolkijju876")
    user5 = User(user_name = "Hessu Hooponen :-) ", user_password="K8Hyf43HVruj47")
    user6 = User(user_name = "Juha von Engineer", user_password="vl75dJrVh90765d")

    # Add model to the session
    db.session.add_all([user1, user2, user3, user4, user5, user6])

    # Save session to database with commit
    db.session.commit()

    upload = hub.models.create_static_folder()
    print("Copying images to : " + upload)

    # Add photos of photo_list (collected from defined folder in path) for user in database
    # and commit to database
    photo_list = hub.models.getPhotoData(upload)    
    for im in photo_list:
        photo = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"], is_private=True)
        db.session.add(photo)
        db.session.commit()

# -----------------------------------------------------------

def _get_image():
    location = "C:\\PWBproject\\ImageAnnotator\\tests\\"
    imagefilename = 'kuha meemi1.jpg'
    with open(location + imagefilename, "rb") as f:
        image_binary = f.read()
        image_ascii = base64.b64encode(image_binary).decode('ascii')
        timestamp = os.path.getctime(imagefilename)
        datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        image_dict = {
            "image_data": image_binary,
            "image_ascii": image_ascii,
            "name": imagefilename,
            "publish_date": datetime.fromisoformat(datetime_str),
            "location": location,
            "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        return image_dict

def _get_user_json():
    """
    Creates a valid user JSON object to be used for PUT and POST tests.
    """
    #return  {
	#        "id": 1,
    #        "user_name": "tester2",
    #        "user_password": "nhyfi87539hldr"
    #        }
    return  {	        
            "user_name": "tester2",
            "user_password": "nhyfi87539hldr"
            }            

"""
def _get_image_json():
    return  {
	        "id": 1,
            "user_id": 2,
            "name": "johanna",
            "publish_date": "2021-04-14 11:00:12",
            "location": "D:\\000web\\ImageAnnotator\\data\\ImageTest\\johanna.jpg",
            "is_private": false,
            "date": "2021-04-14 11:00:12"
            }
"""            

def _get_photo_json():    
    request = {"user_name": "Meria Developer","is_private":True}
    local_file_to_send = 'C:\\PWBproject\\ImageAnnotator\\data\\PhotoTest\\Norja 2020.jpg'
    content = {
     'request': json.dumps(request),
     'image': (os.path.basename(local_file_to_send), open(local_file_to_send, 'rb'), 'application/octet-stream')
    }
    return content

def _get_image_json():
    return  1

def _get_photoannotation_json():    # NO IMPLEMENTATION
    return  1

def _get_imageannotation_json():
    return  1


#def _get_sensor_json(number=1):
#    """
#    Creates a valid sensor JSON object to be used for PUT and POST tests.
#    """
#    return {"name": "extra-sensor-{}".format(number), "model": "extrasensor"}
    
def _check_namespace(client, response):
    """
    Checks that the "annometa" namespace is found from the response body, and
    that its "name" attribute is a URL that can be accessed.
    """
    ns_href = response["@namespaces"]["annometa"]["name"]
    print("check namespaces:", ns_href)
    resp = client.get(ns_href)
    print("check namespaces:", resp)
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
    
def _check_control_put_method(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
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
    
def _check_control_post_method(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
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
    print("_check_control_post_method: href : " + href)
    print("_check_control_post_method: body : " + str(body))
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_post_for_photo_method(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
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
    body = _get_photo_json()    
    resp = client.post(href, data=body, content_type="multipart/form-data")    
    assert resp.status_code == 200


#############################################################################
# test User and User Collection Resources

class TestUserCollection(object):

    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        print("class TestUserCollection RESOURCE_URL:", resp)
        print("class TestUserCollection - resp.status_code", resp.status_code)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        print("class TestUserCollection BODY:", body)
        _check_namespace(client, body)
        _check_control_post_method("annometa:add-user", client, body)
        assert len(body["items"]) == 6  # 6 users in database
        for item in body["items"]:
            _check_control_get_method("self", client, item)
            _check_control_get_method("profile", client, item)

    def test_post(self, client):
        valid = _get_user_json()
        
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["user_name"] + "/")
        resp = client.get(resp.headers["Location"]) # TARVIIKO MUUTTAA 
        assert resp.status_code == 200
        
        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # remove model field for 400
        valid.pop("user_password")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
class TestUserItem(object):

    RESOURCE_URL = "/api/users/Meria%20Developer/"
    INVALID_URL = "/api/users/who-joanna/"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("collection", client, body)
        _check_control_put_method("edit", client, body)
        _check_control_delete_method("annometa:delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        valid = _get_user_json()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with another user's name
        valid["user_name"] = "Juhis Engineer"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # test with valid (only change user_name)
        valid["user_name"] = "Meria Developer"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("user_password")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
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
        print("Test Photocollection Print out of body ", body)
        _check_namespace(client, body)
        _check_control_post_for_photo_method("annometa:add-photo", client, body)
        assert len(body["items"]) > 0
        for item in body["items"]:
            assert "id" in item
            assert "user_id" in item
            assert "name" in item
            assert "publish_date" in item
            assert "location" in item
            assert "is_private" in item
            assert "date" in item

    
    def test_post(self, client):
        
        # Tests the POST method. 
        # Checks all of the possible error codes, 
        # and also checks that a valid request receives a 201 response with a location header 
        # that leads into the newly created resource.
        
        body = _get_photo_json()

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")        
        data_dict = json.loads(client.get(self.RESOURCE_URL).data)
        id = data_dict["items"][-1]["id"]
        assert resp.status_code == 200        
        #assert resp.headers["Location"].endswith(self.RESOURCE_URL + str(id) + "/") # ei voi tehdä, koska ei ole photoid talletettu Rsponse headeriin
        # resp = client.get(resp.headers["Location"]) # sama syy
        # assert resp.status_code == 200 # sama syy
        # body = json.loads(resp.data) 

        #    mitä tähän merkitään ?       ##############################

        #assert body["id"] == 3
        
                
        #assert body["location"] == "xxx"
        #assert body["is_private"] == "xxx xxx"
        #assert body["date"] == "xxxx"

        # test with wrong content type (data must be a dictionary with json part and binary part)
        resp = client.post(self.RESOURCE_URL, data=body, content_type="application/json")
        assert resp.status_code == 400
        
        # remove user_name field for 400
        req_str = body["request"]
        req_dict = json.loads(req_str)
        req_dict["user_name"] = ""
        body["request"] = json.dumps(req_dict)        
        
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        assert resp.status_code == 400

    
class TestPhotoItem(object):
    
    RESOURCE_URL = "/api/photos/1/"
    INVALID_URL = "/api/photos/x/"
    MODIFIED_URL = "/api/photos/30/"
    
    def test_get(self, client):
        
        # Tests the GET method. 
        # Checks that the response status code is 200, 
        # and then checks that all of the expected attributes and controls are present, 
        # and the controls work. 
        # Checks that all items of database populuation are present, 
        # and checks that all their controls are present.
        
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)

        #    mitä tähän merkitään ?       ##############################
        print("Test PhotoItem - print out of body ", body)
        assert body["id"] == 1        
        assert "\\static\\images\\" in body["location"]
        assert body["is_private"] == True
        

        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("collection", client, body)
        #_check_control_put_method_photo("edit", client, body) NOT implemented in resource.py
        _check_control_delete_method("annometa:delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404
    """      
    def test_put(self, client):
        
        # Tests the PUT method. 
        # Checks all of the possible error codes, 
        # and also checks that a valid request receives a 204 response. 
        # Also tests that when name is changed, the photo can be found from a its new URI. 
        
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
        
        # Tests the DELETE method. 
        # Checks that a valid request reveives 204 response, 
        # and that trying to GET the photo afterwards results in 404.
        # Also checks that trying to delete a photo that doesn't exist results in 404.
        
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
    """
        
        
        
        
        
        
        
        
        
        
    
    

    

        
            
    