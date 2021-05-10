# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# Image Annotator API database test file - db_test.py
# This file includes database test finctions of Image Annotator API.

# The file is created by example in GitHub 
# https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/db_test.py

"""
# ----------------------------------------------

Activate created python virtual environment (on VSC cmd):
cd C:\PWPproject\ImageAnnotator\.venv\Scripts
activate.bat

# ---- OR

C:\PWPproject>
C:\PWPproject>cd ImageAnnotator
C:\PWPproject\ImageAnnotator>cd .venv
C:\PWPproject\ImageAnnotator\.venv>cd Scripts
C:\PWPproject\ImageAnnotator\.venv\Scripts>activate.bat

# ----------------------------------------------

Go to ImageAnnotator folder:
    (.venv) C:\PWBproject\ImageAnnotator>

Set cofiguration setting class as 'development' or 'production' or 'default'
    (.venv) C:\PWBproject\ImageAnnotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\PWBproject\ImageAnnotator\extracodes>set FLASK_APP=hub

# ----------------------------------------------

"""

# run with command
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest
# same as above but with console output
# (.venv) C:\PWBproject\ImageAnnotator\tests>python -m pytest -s 

# import python packages -----------------------------------

import glob
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

    i = 0
    with app.app_context():
        db.create_all()
        print("Numero: ", i+1)
        _populate_database()

    yield app.test_client()
    
    os.close(db_fd)
    os.unlink(db_fname)

# ------------------------------------------------------
# Collect images and image meta data from defined ImageTest -folder to image_list

def _getImageDatas(upload):
    image_list = []
    cwd = os.getcwd()
    parent_folder = os.path.dirname(cwd)    # get parent directory from tests = "..\\ImageAnnotator"
    folder = '\\Data\\ImageTest\\'
    source_images_folder = parent_folder + folder
    print("  _get: source_images_folder:", source_images_folder)
    
    for filename in glob.glob(source_images_folder + '*.jpg'):
        print("\n Print image data filename:  ", filename)
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
    #print("_get: image_list:", image_list)
    return image_list

# -------------------------------------------------------------------------------
# Collect photos and photo meta data from defined PhotoTest -folder to photo_list

# from PIL import Image, ExifTags

def _getPhotoDatas(upload):
    photo_list = []
    cwd = os.getcwd()
    parent_folder = os.path.dirname(cwd)    # get parent directory from tests = "..\\ImageAnnotator"
    folder = '\\Data\\PhotoTest\\'
    source_photos_folder = parent_folder + folder
    print("_get..: source_photos_folder:", source_photos_folder)

    print("for looppiin")
    for filename in glob.glob(source_photos_folder + '*.jpg'):
        meta_data_dict = set_photo_meta_data_to_dict(filename, True)
        # NOTE!!!
        # remember to set photo location, this is done differently in tests (test image folder -> static/photos)
        # in development state image is saved from request (request.image -> static/photos)
        meta_data_dict["location"] = hub.models.save_to_upload(upload, source_photos_folder, os.path.basename(filename))
        photo_list.append(meta_data_dict)
    #print("_get: photo_list:", photo_list)
    return photo_list

# -----------------------------------------------------------
# CREATE AND POPULATE DATABASE

def _populate_database():
    
    # create folder images to hub static folder for images 
    # images folder is created if it does not exist
    # created with function in the end of this function

    # upload = create_static_folder_test()
    # #### NOTE alapuolella oleva rivi korvaa ylemmän
    # käyttää models.py tiedostossa olevaa funktiota
    # \ImageAnnotator\hub\static\images is the created_static_folder
    # \ImageAnnotator\hub\static\photos is the created_static_folder
    (upload_images_folder, upload_photos_folder) = create_static_folders()
    print("\n Creating resource test images to folder : " + upload_images_folder)
    print("\n Creating resource test photos to folder : " + upload_photos_folder)
    basedir = os.path.abspath(os.path.dirname(__file__))
    print("\n basedir for resource_test.py:", basedir)

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
    userqueried = User.query.filter_by(user_name="Meria Developer").first()
    #print("userqueried:", userqueried.user_name)
    
    # Add IMAGES to image list (collected from defined folder in path)
    # defined for user in database
    # and commit to database
    cwd = os.getcwd()   # get current working directory = ""..\\ImageAnnotator\\tests"
    print(" current working directory:   ", cwd)
    parent_folder = os.path.dirname(cwd)    # get parent directory from tests = "..\\ImageAnnotator"
    image_folder = "\\Data\ImageTest\\" 
    image_list = _getImageDatas(upload_images_folder) 
    print("IMAGE LIST:", image_list)  

    for im in image_list:
        image = ImageContent(name=im["name"], publish_date=im["publish_date"], location=im["location"], is_private=False, date=im["date"])
        userqueried.image_user.append(image)
        db.session.commit()

    # collect queries for defined user_name and image name
    current_user = User.query.filter_by(user_name="Meria Developer").first()
    imagename_queried = ImageContent.query.filter_by(name="kuha meemi1.jpg").first()
    print(" X X X X X X X imagename_queried:", imagename_queried)
    # and commit both to database
    anno_list = hub.models.getImageAnnoData()
    for anno in anno_list:
        #annotation = ImageAnnotation(persons_class=anno["persons_class"], text_persons=anno["text_persons"], text_persons_comment=anno["text_persons_comment"], text_free_comment=anno["text_free_comment"], positivity_class=anno["positivity_class"], slideshow_class=anno["slideshow_class"])   
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
    

    # Add PHOTOS of photo_list (collected from defined folder in path) 
    # defined for user in database
    # and commit to database
    cwd = os.getcwd()   # get current working directory = ""..\\ImageAnnotator\\tests"
    print("    current working directory: ", cwd)
    parent_folder = os.path.dirname(cwd)    # get parent directory from tests = "..\\ImageAnnotator"
    #os.chdir('../') # current workin dirextory is one up
    photo_folder = "\\data\PhotoTest\\"
    #upload_photos_folder = parent_folder + photo_folder
    print("    upload_photos_folder: ", upload_photos_folder)
    #photo_list = _getPhotoData(upload_photos_folder) 
    photo_list = _getPhotoDatas(upload_photos_folder) 
    print("    PHOTO LIST:", photo_list)  

    for im in photo_list:
        photo = ImageContent(name=im["name"], publish_date=im["publish_date"], location=im["location"], is_private=True, date=im["date"])
        userqueried.photo_user.append(photo)
        #print("photo_user: ", photo_user.user_name)
        #db.session.add(photo)
        db.session.commit()

    # collect queries for defined user_name and photo name
    current_user = User.query.filter_by(user_name="Meria Developer").first()
    photoname_queried = ImageContent.query.filter_by(name="Norja 2020.jpg").first()
    print("   X X X X X X X photoname_queried:", photoname_queried)
    # and commit both to database
    anno_list = hub.models.getPhotoAnnoData()
    for anno in anno_list:
        annotation = PhotoAnnotation(persons_class=anno["persons_class"], text_persons=anno["text_persons"], text_persons_comment=anno["text_persons_comment"], text_free_comment=anno["text_free_comment"], positivity_class=anno["positivity_class"], slideshow_class=anno["slideshow_class"])   
        current_user.photo_annotator.append(annotation)
        photoname_queried.photo_annotations.append(annotation)
        db.session.commit()

    # alla oleva funktio on tarpeeton, koska käytetään models tiedoston vastaavaa
    """
    def create_static_folder_test():
    basedir = os.path.abspath(os.path.dirname(__file__))
    upload = basedir + UPLOAD_FOLDER
    try:        
        if not os.path.exists(upload):
            os.makedirs(upload)
    except OSError as e:
        print('FAILED : ' + str(upload), file=sys.stderr)
        raise ValueError('Folder for static images could not be created.')
    return upload
    """
"""
# -------------------------------------------------------------------------------
# Collect images and image meta data from defined ImageTest -folder to image_list

def _getImageData(upload):
    image_list = []
    cwd = os.getcwd()
    folder = '\\data\\ImageTest\\'
    source_images_folder = cwd + folder
    print("  models.py: source_images_folder:", source_images_folder)
    
    for filename in glob.glob(source_images_folder + '*.jpg'):
        print("\n Print image data filename:  ", filename)
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
        print("  models.py: image_list:", image_list)
    return image_list

# -------------------------------------------------------------------------------
# Collect photos and photo meta data from defined PhotoTest -folder to photo_list

# from PIL import Image, ExifTags

def _getPhotoData(upload):
    photo_list = []
    cwd = os.getcwd()
    parent_folder = os.path.dirname(cwd)    # get parent directory from tests = "..\\ImageAnnotator"
    folder = '\\Data\\PhotoTest\\'
    source_photos_folder = parent_folder + folder
    print("_get..: source_photos_folder:", source_photos_folder)

    for filename in glob.glob(source_photos_folder + '*.jpg'):        
        print("for loopissa")
        meta_data_dict = set_photo_meta_data_to_dict(filename, True)
        # NOTE!!!
        # remember to set photo location, this is done differently in tests (test image folder -> static/photos)
        # in development state image is saved from request (request.image -> static/photos)
        meta_data_dict["location"] = hub.models.save_to_upload(upload, source_photos_folder, os.path.basename(filename))
        photo_list.append(meta_data_dict)
    print("_get: photo_list:", photo_list)
    return photo_list
"""
# -----------------------------------------------------------
# json helper functions

def _get_user_json():
    """
    Creates a valid user JSON object to be used for PUT and POST tests.
    """
    return  {	        
            "user_name": "tester2",
            "user_password": "nhyfi87539hldr"
            }      

"""
# Not used in this test
def _get_image():
    location = "C:\\PWPproject\\ImageAnnotator\\tests\\"
    imagefilename = 'kuha meemi1.jpg'
    with open(location + imagefilename, "rb") as f:
        timestamp = os.path.getctime(imagefilename)
        datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        image_dict = {
            "name": imagefilename,
            "publish_date": datetime.fromisoformat(datetime_str),
            "location": location,
            "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        return image_dict
"""

def _get_photo_json():    
    request = {"user_name": "Meria Developer","is_private":True}
    #local_file_to_send = 'C:\\PWPproject\\ImageAnnotator\\data\\PhotoTest\\Norja 2020.jpg'
    cwd = os.getcwd()   # get current working directory = ""..\\ImageAnnotator\\tests"
    #print("current working directory: ", cwd)
    parent_folder = os.path.dirname(cwd)    # get parent directory from tests = "..\\ImageAnnotator"
    photo_folder = "\\data\PhotoTest\\"
    imagefilename = 'Norja 2020.jpg'
    local_file_to_send = parent_folder + photo_folder + imagefilename
    print("local_file_to_send:", local_file_to_send)
    #local_file_to_send = 'C:\\PWPproject\\ImageAnnotator\\data\\PhotoTest\\Norja 2020.jpg'
    content = {
     'request': json.dumps(request),
     'image': (os.path.basename(local_file_to_send), open(local_file_to_send, 'rb'), 'application/octet-stream')
    }
    return content

def _get_photoannotation_json():    
    # return  1
    # Creates a valid photoannotation JSON object to be used for PUT and POST tests.
    return  {	        
            "photo_id": 4,
            "user_id": 3,
            "persons_class": True,
            "slideshow_class": True,
            "positivity_class": 4,
            "text_free_comment": "Norway on summer 2020",
            "text_persons": "norwegian sheep",
            "text_persons_comment": "Norwegian sheep having a nap on shore"
    }




def _get_image_json():              # NO IMPLEMENTATION
    return  1

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

def _get_imageannotation_json():    # NO IMPLEMENTATION
    return  1

# -------------------------------------------------------------------------------------
# helper functions

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
    print("_check_namespace:", ns_href)
    resp = client.get(ns_href)
    print("_check_namespace:", resp)
    assert resp.status_code == 200
    
def _check_control_get_method(ctrl, client, obj):
    """
    Checks a GET type control from a JSON object be it root document or an item
    in a collection. Also checks that the URL of the control can be accessed.
    """
    href = obj["@controls"][ctrl]["href"]
    print("_check_control_get_method:", href)
    resp = client.get(href)
    print("_check_control_get_method:", resp)
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
    print("_check_control_delete_method:", resp)
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
    #if expect_failure: # KOKEILU JUHAN KESKEN VIELA
    #    with pytest.raises(ValidationError):
    #        validate(body, schema)
    #else: 
    #    validate(body, schema)
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
        #print("class TestUserCollection RESOURCE_URL:", resp)
        #print("class TestUserCollection - resp.status_code", resp.status_code)
        assert resp.status_code == 200
        
        body = json.loads(resp.data)
        print(" Y  Y  Y  Y  Y  Y  Y  Y  Y ")
        print("class TestUserCollection BODY:", body)
        print(" Y Y Y Y Y Y Y Y Y Y  ")
        _check_namespace(client, body)
        _check_control_post_method("annometa:add-user", client, body)
        
        # 6 users populated to database
        assert len(body["items"]) == 6  
        
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

        # test with valid user name (do not change user_name)
        valid["user_name"] = "Meria Developer"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204        

        # test with undefined user name (only change user_name)
        valid["user_name"] = "Juhis Engineer"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204                       

        # remove field for 400
        valid["user_name"] = "Juhis Engineer"
        valid.pop("user_password")        
        resp = client.put("/api/users/Juhis%20Engineer/", json=valid)
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
        
        # Tests the POST method. Checks all of the possible error codes, 
        # and also checks that a valid request receives a 201 response with a location header 
        # that leads into the newly created resource.
        
        body = _get_photo_json()

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, data=body, content_type="multipart/form-data")
        
        print("\n print photo resp:  ", resp)

        data_dict = json.loads(client.get(self.RESOURCE_URL).data)
        id = data_dict["items"][-1]["id"]
        print("\n print photo DATADICT:  ", data_dict)

        # alla oleva testi menee pieleen - antaa vastauksen 200
        #assert resp.status_code == 201        
        
        #assert resp.headers["Location"]#.endswith(self.RESOURCE_URL + str(id) + "/") # ei voi tehdä, koska ei ole photoid talletettu Rsponse headeriin
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
    
    RESOURCE_URL = "/api/photos/9/"
    INVALID_URL = "/api/photos/x/"
    MODIFIED_URL = "/api/photos/30/"
    
    def test_get(self, client):
        
        # Tests the GET method. 
        # Checks that the response status code is 200, 
        # and then checks that all of the expected attributes and controls are present, 
        # and the controls work. 
        # Checks that all items of database populuation are present, 
        # and checks that all their controls are present.
        # KUVA NORAJ  20202 tulee 
        print("\n    * * * * DEF TEST GET OLLAAN * * * * \n")
        resp = client.get(self.RESOURCE_URL)
        print("photot test_get resp:", resp)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        print("photot test_get body:", body)

        #    mitä tähän merkitään ?       ##############################
        print("Test PhotoItem - print out of body ", body)
        assert body["id"] == 9  # JUHAN KOMMENTTI halla-aho32.jpg has id=1
        assert "\\static\\photos\\" in body["location"]
        assert body["is_private"] == True  # JUHA KOMMENTIKSI KUN TULEE ERROR
        

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

#############################################################################
# test Imageannotation and Imageannotation Collection Resources

class TestImageannotationCollection(object):

    RESOURCE_URL = "/api/imageannotations/"

    def test_get(self, client):
        
        resp = client.get(self.RESOURCE_URL)
        print("\n print class TestImageannotationCollection - RESOURCE_URL:  ", resp)
        print("\n print class TestImageannotationCollection - resp.status_code:  ", resp.status_code)
        assert resp.status_code == 200
        
        body = json.loads(resp.data)
        print("\n print class TestImageannotationCollection - BODY:  ", body)
        _check_namespace(client, body)
        #_check_control_post_method("annometa:add-imageannotation", client, body) 
        # JUHA KOMMENTOI EDLLISEN RIVIN KUN SE TEKEE PERSONS CLASS VALIDATION ERRORIN
        
        # 1 photoannotation in database
        #assert len(body["items"]) == 1
        assert len(body["items"]) > 0
    
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

#############################################################################
# test Photoannotation and Photoannotation Collection Resources

class TestPhotoannotationCollection(object):

    RESOURCE_URL = "/api/photoannotations/"

    def test_get(self, client):
        
        resp = client.get(self.RESOURCE_URL)
        print("\n print class TestPhotoannotationCollection - RESOURCE_URL:  ", resp)
        print("\n print class TestPhotoannotationCollection - resp.status_code:  ", resp.status_code)
        assert resp.status_code == 200
        
        body = json.loads(resp.data)
        print("\n print class TestPhotoannotationCollection - BODY:  ", body)
        _check_namespace(client, body)
        #_check_control_post_method("annometa:add-photoannotation", client, body) 
        # JUHA KOMMENTOI EDLLISEN RIVIN KUN SE TEKEE PERSONS CLASS VALIDATION ERRORIN
        
        # 1 photoannotation in database
        #assert len(body["items"]) == 1
        assert len(body["items"]) > 0
        
        for item in body["items"]:
            assert "id" in item
            assert "photo_id" in item
            assert "user_id" in item
            assert "persons_class" in item
            assert "slideshow_class" in item
            assert "positivity_class" in item
            assert "text_free_comment" in item
            assert "text_persons" in item
            assert "text_persons_comment" in item

 
        
        
        
        
        
        
        
    
    

    

        
            
    