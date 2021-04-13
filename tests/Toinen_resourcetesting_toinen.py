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
import glob
import base64
from io import BytesIO
from PIL import Image, ExifTags

from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

# import api files and functions -----------------------

#from app import create_app, db
#import app
from hub import create_app, db
from hub.models import User, ImageContent, ImageAnnotation, PhotoAnnotation

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# ------------------------------------------------------
# define and use testing confuguration
# based on http://flask.pocoo.org/docs/1.0/testing/
# client is not neeeded for database and resources testing
# db handle is needed for db and resource testing

# code below copied and applied from sensorhub github

@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()    
    
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    app = create_app(config)

    with app.app_context():
        db.create_all()
        populate_database()
        
    yield app.test_client()

    os.close(db_fd)
    os.unlink(db_fname)

# ------------------------------------------------------
# CREATE AND POPULATE DATABASE

def populate_database():
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

# -------------------------------------------------------------------
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