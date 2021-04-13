# define resources here
import os
import json
from jsonschema import validate, ValidationError
from datetime import datetime
from pathlib import Path, PurePath

from flask import Response, request, url_for, abort
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from io import BufferedReader
# needed for image validation
from werkzeug.utils import secure_filename

#from hub import db or database
import sys
#import hub.api_routes
#from hub.api_routes import *

from hub.constants import *

import hub.models
from hub.models import *

import hub.utils
from hub.utils import *


### User and User Collection Resources ---------------------------------------

# check database and db table names !!!!!!!!!!!!!!

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

class UserCollection(Resource):
    """
    Resource for UserCollection. 
    Function GET gets all the users in collection
    and function POST adds a new user to collection.
    """

    def get(self):
        """
        GET method gets all the users from collection
        """
        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        #
        body.add_control("self", url_for("api.usercollection"))
        body.add_control_add_user()
        body["items"] = []
        for db_user in User.query.all():
            item = HubBuilder(
                user_name=db_user.user_name,
                user_password=db_user.user_password
            )
            item.add_control("self", url_for("api.usercollection"))
            item.add_control("profile", USER_PROFILE)
            body["items"].append(item)
        return Response(json.dumps(body), status=200, mimetype=MASON)


    def post(self):
        """
        POST method adds a new user to collection
        """
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.user_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        new_user = User(
            user_name=request.json["user_name"],
            user_password=request.json["user_password"]
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Username already exists", "User with name '{}' already exists in database. Choose new username.".format(request.json["user_name"]))

        # tarkista alla oleva rivi !!!
        return Response(status=201, headers={"Location": url_for("api.useritem", name=request.json["user_name"])})


class UserItem(Resource):
    """
    Resource for single UserItem. 
    Function GET gets a user, PUT edits a user and DELETE deletes a user.
    """
    def get(self, user_name):
        """
        GET method gets a single user
        """
        db_user = User.query.filter_by(user_name=user_name).first()
        if db_user is None:
            return create_error_response(404, "Not found", "No user was found with name {}".format(user_name))

        body = HubBuilder(
            user_name=db_user.user_name,
            user_team=db_user.user_team
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.useritem", user_name=user_name))
        body.add_control("profile", USER_PROFILE)
        body.add_control("collection", url_for("api.usercollection"))
        body.add_control_delete_user(user_name)
        body.add_control_edit_user(user_name)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def put(self, user_name):
        """
        PUT method edits a user
        """
        db_user = User.query.filter_by(user_name=user_name).first()
        if db_user is None:
            return create_error_response(404, "Not found", "No user was found with name {}".format(user_name))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.user_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_user.user_name = request.json["user_name"]
        db_user.user_password = request.json["user_password"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Username already exists", "User with name '{}' already exists in database. Choose new username.".format(request.json["user_name"]))

        return Response(status=204)

    def delete(self, user_name):
        """
        DELETE method deletes a user
        """
        db_user = User.query.filter_by(user_name=user_name).first()
        if db_user is None:
            return create_error_response(404, "Not found", "No user was found with name {}".format(user_name))

        db.session.delete(db_user)
        db.session.commit()

        return Response(status=204)


### Photo and Photo Collection Resources ---------------------------------------

# check database and db table names !!!!!!!!!!!!!!

class PhotoCollection(Resource):
    """
    Resource for PhotoCollection. 
    Function GET gets all the photos in collection
    and POST adds a new photo to collection.
    """

    def get(self):
        """
        GET method gets all the photos from PhotoCollection
        """

        # reqeusttissa pitää tulla tieto, jakeeko käyttäjä imageja vai photoja
        # haku kantaan tehdään siten, että haetaan kuvat käyttäen is_private -lippua

        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.photocollection"))
        body.add_control_add_photo()
        body["items"] = []
        
        for photo in ImageContent.query.filter(ImageContent.is_private == True):
        #for photo in ImageContent.query.all():

        #for photo in ImageContent.query.filter(ImageContent.is_private==request.json["is_private"]):

            #if ImageContent.is_private == TRUE:
            # tässä kohdassa on mahdollista filteröidä ja erotella kuvat ja photot is_private lipun ja requestissa tulleen _is_provate lipun välillä
            # mutta parempi olisi erotella kuvat suoraan tietokantakyselyssä
            item = HubBuilder(
                id = photo.id,
                user_id = photo.user_id,
                #data = photo.data,
                #ascii_data = photo.ascii_data,
                name = photo.name,
                publish_date = photo.publish_date,
                location = photo.location,
                is_private = photo.is_private,
                date = photo.date
            )

            item.add_control("self", url_for("api.photocollection"))
            item.add_control("profile", PHOTO_PROFILE)
            body["items"].append(item)
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)


    def post(self):
        """
        POST method adds a new photo to collection
        """
        #if not request.json:
        #    return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        #try:
        #    validate(request.json, HubBuilder.photo_schema())
        #except ValidationError as e:
        #    return create_error_response(400, "Invalid JSON document", str(e))

        # hae sisään kirjautunut käyttäjä
        
        
        try:
            req_content = json.loads(request.form['request'])
        except Exception as e:
            print('exp : ' + str(e), file=sys.stderr)    
            return create_error_response(400, "Invalid JSON document", str(e))                
        
        currentUser = User.query.filter_by(user_name=req_content["user_name"]).first()
        print('currentUser : ' + str(currentUser), file=sys.stderr)
        # check if there's a file in the requst
        
        # check if the post request has the file part
        if 'image' not in request.files:
            return create_error_response(400, "No file provided", "No image file found in the request")

        image = request.files['image']
        if image.filename == '':
            return create_error_response(400, "No file provided", "No image file found in the request")
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # here we could check if the file exists already
            # return error response if it does OR rename the file by adding a datetime to its name                        
            basedir = os.path.abspath(os.path.dirname(__file__))
            
            upload = basedir + UPLOAD_FOLDER + filename
            
            # hae location tieto request.json["location"]
            # hae name tieto request.json["name"]
            # avaa file ja palauta se ascii ja binary muodossa sekä kuvan metadata
            image.save(upload)
            photo_item = hub.utils.convert_image_to_db_object(upload, upload, filename, req_content["is_private"])            

            try:
                currentUser.photo_user.append(photo_item)
                db.session.commit()                                
            except IntegrityError:
                return create_error_response(409, "Already exists", "Photo with id '{}' already exists".format(request.json["id"]))
            except Exception as e:
                create_error_response(500, "Failed to save the file", str(e) + " Failed to save file '{}'".format(request.json["id"]))
            
            # -------------- alla oleva lause on väärin -------------------------------------
            #return Response(status=201, headers={"Location": url_for("api.photoitem", id=request.json["id"])})
            #return Response(status=201, headers={"Location": api.url_for(PhotoItem, id=request.json["id"])})
            #return Response(status=201, headers={"Location": url_for("PhotoItem", id=request.json["id"])})
            #return Response(status=201, headers={"Location": url_for("photoitem", id=request.json["id"])})
            #return Response(status=201, headers={"Location": url_for("api.PhotoiItem", id=request.json["id"])})

            #return Response(status=201, headers={"Location": url_for("api.photoitem", photo=request.json["name"])})
            return Response(status=201, headers={"Location": url_for("api.photoitem", photo_item=upload)})

            # TARKISTA - harjoituksista miten url_for muodostetaan yllä olevaan lauseeseen !!!!!!!!!!!!!!!!!

class PhotoItem(Resource):
    """
    Resource for PhotoItem. 
    Function GET gets one single photo, PUT edits the photo,
    and DELETE deletes the photo.
    """
    def get(self, id):
        """
        GET method gets one single photo
        """
        db_photoid = Photo.query.filter_by(id=id).first()
        if db_photoid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))

        body = HubBuilder(
                id = db_photoid.id,
                user_id = db_photoid.user_id,
                data = db_photoid.data,
                ascii_data = db_photoid.ascii_data,
                name = db_photoid.name,
                publish_date = db_photoid.publish_date,
                location = db_photoid.location,
                is_private = db_photoid.is_private,
                date = db_photoid.date
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.photoitem", id=id))
        body.add_control("profile", PHOTO_PROFILE)
        body.add_control("collection", url_for("api.photocollection"))
        body.add_control_delete_photo(id)
        body.add_control_edit_photo(id)

        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)

    def put(self, id):
        """
        PUT method edits a single photo 
        """
        db_photoid = Photo.query.filter_by(id=id).first()

        if db_photoid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.photo_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_photoid.id = request.json["id"],
        db_photoid.user_id = request.json["user_id"],
        db_photoid.data = request.json["data"],
        db_photoid.ascii_data = request.json["ascii_data"],
        db_photoid.name = request.json["name"],
        db_photoid.publish_date = request.json["publish_date"],
        db_photoid.location = request.json["location"],
        db_photoid.is_private = request.json["is_private"],
        db_photoid.date = request.json["date"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Photo with id '{}' already exists".format(request.json["id"]))
        return Response(status=204)


    def delete(self, id):
        """
        DELETE method deletes a single photo
        """
        db_photoid = Photo.query.filter_by(id=id).first()
        if db_photoid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))

        db.session.delete(db_photoid)
        db.session.commit()

        return Response(status=204)


# -----------------------------------------------------------------------------------------------
### Photoannotation and Photoannotation Collection Resources --------------------------------------

# check database and db table names !!!!!!!!!!!!!!

class PhotoannotationCollection(Resource):
    """
    Resource for PhotoannotationCollection. 
    Function GET gets all the photoannotations in collection
    and POST adds a new photoannotation to collection.
    """

    def get(self):
        """
        GET method gets all the photoannotations from PhotoannotationCollection
        """
        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.photoannotationcollection"))
        body.add_control_add_photoannotation()
        body["items"] = []

        for db_photoanno_id in PhotoAnnotation.query.all():
            item = HubBuilder(
                id = db_photoanno_id.id,
                photo_id = db_photoanno_id.photo_id,
                user_id = db_photoanno_id.user_id,
                persons_class = db_photoanno_id.persons_class,
                slideshow_class = db_photoanno_id.slideshow_class,
                positivity_class = db_photoanno_id.positivity_class,
                text_free_comment = db_photoanno_id.text_free_comment,
                text_persons = db_photoanno_id.text_persons,
                text_persons_comment = db_photoanno_id.text_persons_comment
            )

            item.add_control("self", url_for("api.photoannotationcollection"))
            item.add_control("profile", PHOTOANNOTATION_PROFILE)
            body["items"].append(item)
        
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)
        

    def post(self):
        """
        POST method adds a new photoannotation to collection
        """
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.photoannotation_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        new_photoannotation = Photoannotation(
            id = request.json["id"],
            photo_id = request.json["photo_id"],
            user_id=request.json["user_id"],
            persons_class = request.json["persons_class"],
            slideshow_class = request.json["slideshow_class"],
            positivity_class = request.json["positivity_class"],
            text_free_comment = request.json["text_free_comment"],
            text_persons = request.json["text_persons"],
            text_persons_comment = request.json["text_persons_comment"]
        )
        try:
            db.session.add(new_photoannotation)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Photoannotation with id '{}' already exists".format(request.json["id"]))
        return Response(status=201, headers={"Location": url_for("api.photoannotationitem", id=request.json["id"])})


class PhotoannotationItem(Resource):
    """
    Resource for PhotoannotationItem. 
    Function GET gets one single photoannotation, PUT edits the photoannotation,
    and DELETE deletes the photoannotation.
    """

    def get(self, id):
        """
        GET method gets one single photoannotation
        """
        db_photoanno_id = PhotoAnnotation.query.filter_by(id=id).first()
        if db_photoanno_id is None:
            return create_error_response(404, "Not found", "No photoannotation was found with id {}".format(id))

        body = HubBuilder(
                id = db_photoanno_id.id,
                photo_id = db_photoanno_id.photo_id,
                user_id = db_photoanno_id.user_id,
                persons_class = db_photoanno_id.persons_class,
                slideshow_class = db_photoanno_id.slideshow_class,
                positivity_class = db_photoanno_id.positivity_class,
                text_free_comment = db_photoanno_id.text_free_comment,
                text_persons = db_photoanno_id.text_persons,
                text_persons_comment = db_photoanno_id.text_persons_comment
        )
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.photoannotationitem", id=id))
        body.add_control("profile", PHOTOANNOTATION_PROFILE)
        body.add_control("collection", url_for("api.photoannotationcollection"))
        body.add_control_delete_photoannotation(id)
        body.add_control_edit_photoannotation(id)

        return Response(json.dumps(body), status=200, mimetype=MASON)


    def put(self, id):
        """
        PUT method edits one single photoannotation
        """
        db_photoanno_id = PhotoAnnotation.query.filter_by(id=id).first()
        if db_photoanno_id is None:
            return create_error_response(404, "Not found", "No photoannotation was found with id {}".format(id))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.photoannotation_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_photoanno_id.id = request.json["id"],
        db_photoanno_id.photo_id = request.json["photo_id"],
        db_photoanno_id.user_id=request.json["user_id"],
        db_photoanno_id.persons_class = request.json["persons_class"],
        db_photoanno_id.slideshow_class = request.json["slideshow_class"],
        db_photoanno_id.positivity_class = request.json["positivity_class"],
        db_photoanno_id.text_free_comment = request.json["text_free_comment"],
        db_photoanno_id.text_persons = request.json["text_persons"],
        db_photoanno_id.text_persons_comment = request.json["text_persons_comment"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Photoannotation with id '{}' already exists".format(request.json["id"]))
        return Response(status=204)


    def delete(self, id):
        """
        DELETE method deletes one single photoannotation
        """
        db_photoanno_id = PhotoAnnotation.query.filter_by(id=id).first()
        if db_photoanno_id is None:
            return create_error_response(404, "Not found", "No photoannotation was found with id {}".format(id))

        db.session.delete(db_photoanno_id)
        db.session.commit()
        return Response(status=204)


### Image and Image Collection Resources ---------------------------------------
# check database and db table names !!!!!!!!!!!!!!

class ImageCollection(Resource):
    """
    Resource for ImageCollection. 
    Function GET gets all the images in collection and POST adds a new image to collection.
    """

    def get(self):
        """
        GET method gets all the images from ImageCollection
        """

        # reqeusttissa pitää tulla tieto, jakeeko käyttäjä imageja vai photoja
        # haku kantaan tehdään siten, että haetaan kuvat käyttäen is_private -lippua

        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.imagecollection"))
        body.add_control_add_image()
        body["items"] = []
        
        for image in ImageContent.query.filter(ImageContent.is_private == False):
        #for db_photoid in Photo.query.all():

            # tässä kohdassa on mahdollista filteröidä ja erotella kuvat ja photot is_private lipun ja requestissa tulleen _is_provate lipun välillä
            # mutta parempi olisi erotella kuvat suoraan tietokantakyselyssä
            item = HubBuilder(
                id = image.id,
                user_id = image.user_id,
                #data = image.data,
                #ascii_data = image.ascii_data,
                name = image.name,
                publish_date = image.publish_date,
                location = image.location,
                is_private = image.is_private,
                date = image.date
            )

            item.add_control("self", url_for("api.imagecollection"))
            item.add_control("profile", IMAGE_PROFILE)
            body["items"].append(item)
        
        # definition default=str below because of datetime objects
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)


    def post(self):
        """
        POST method adds a new image to collection
        """
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.image_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        # query request user with user_name
        currentUser = User.query.filter_by(request.json["user_name"]).first()
                # check if the post request has the file part
        if 'image' not in request.files:
            return create_error_response(400, "No file provided", "No image file found in the request")

        image = request.files['image']
        if image.filename == '':
            return create_error_response(400, "No file provided", "No image file found in the request")
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # here we could check if the file exists already
            # return error REsponse if it does OR rename the file by adding a datetime to its name            
            #filename = request.json["name"]
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)        
            # if "is_private" == TRUE add image to photocollection
            #if request.json["is_private"] == True:
            
            # hae location tieto request.json["location"]
            # hae name tieto request.json["name"]
            # avaa file ja palauta se ascii ja binary muodossa sekä kuvan metadata
            obj_populated = hub.utils.convert_image_to_db_object(image, image_path, filename, request.json["is_private"])            

            try:
                currentUser.img_user.append(obj_populated)
                db.session.commit()
            except IntegrityError:
                return create_error_response(409, "Already exists", "Image with id '{}' already exists".format(request.json["id"]))
            except Exception as e:
                create_error_response(500, "Failed to save the file", str(e) + " Failed to save file '{}'".format(request.json["id"]))
            return Response(status=201, headers={"Location": url_for("api.imageitem", id=request.json["id"])})            


class ImageItem(Resource):
    """
    Resource for ImageItem. 
    Function GET gets one single image, PUT edits the image, and DELETE deletes the image.
    """

    def get(self, id):
        """
        GET method gets one single image
        """
        db_imageid = Image.query.filter_by(id=id).first()
        if db_imageid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))

        body = HubBuilder(
                id = db_imageid.id,
                user_id = db_imageid.user_id,
                data = db_imageid.data,
                ascii_data = db_imageid.ascii_data,
                name = db_imageid.name,
                publish_date = db_imageid.publish_date,
                location = db_imageid.location,
                is_private = db_imageid.is_private,
                date = db_imageid.date
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.imageitem", id=id))
        body.add_control("profile", IMAGE_PROFILE)
        body.add_control("collection", url_for("api.imagecollection"))
        body.add_control_delete_image(id)
        body.add_control_edit_image(id)

        # definition default=str below because of datetime objects
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)


    def put(self, id):
        """
        PUT method edits one single image 
        """
        db_imageid = Image.query.filter_by(id=id).first()
        if db_imageid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.image_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_imageid.id = request.json["id"],
        db_imageid.user_id = request.json["user_id"],
        db_imageid.data = request.json["data"],
        db_imageid.ascii_data = request.json["ascii_data"],
        db_imageid.name = request.json["name"],
        db_imageid.publish_date = request.json["publish_date"],
        db_imageid.location = request.json["location"],
        db_imageid.is_private = request.json["is_private"],
        db_imageid.date = request.json["date"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Image with id '{}' already exists".format(request.json["id"]))
        return Response(status=204)


    def delete(self, id):
        """
        DELETE method deletes one single image
        """
        db_imageid = Image.query.filter_by(id=id).first()
        if db_imageid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))
        
        db.session.delete(db_imageid)
        db.session.commit()

        return Response(status=204)


### Imageannotation and Imageannotation Collection Resources --------------------------------------
# check database and db table names !!!!!!!!!!!!!!

class ImageannotationCollection(Resource):
    """
    Resource for ImageannotationCollection. 
    Function GET gets all the imageannotations in collection
    and POST adds a new imageannotation to collection.
    """

    def get(self):
        """
        GET method gets all imageannotations from ImageannotationCollection
        """
        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.imageannotationcollection"))
        body.add_control_add_imageannotation()
        body["items"] = []
        for db_imageanno_id in ImageAnnotation.query.all():

            item = HubBuilder(
                id = db_imageanno_id.id,
                image_id = db_imageanno_id.image_id,
                user_id = db_imageanno_id.user_id,
                meme_class = db_imageanno_id.meme_class,
                HS_class = db_imageanno_id.HS_class,
                text_class = db_imageanno_id.text_class,
                polarity_classA = db_imageanno_id.polarity_classA,
                polarity_classB = db_imageanno_id.polarity_classB,
                HS_strength = db_imageanno_id.HS_strength,
                HS_category = db_imageanno_id.HS_category,
                text_text = db_imageanno_id.text_text,
                text_language = db_imageanno_id.text_language
            )
            item.add_control("self", url_for("api.imageannotationcollection"))
            item.add_control("profile", IMAGEANNOTATION_PROFILE)
            body["items"].append(item)
        return Response(json.dumps(body), status=200, mimetype=MASON)


    def post(self):
        """
        POST method adds a new imageannotation to collection
        """
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.imageannotation_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        new_imageannotation = Imageannotation(
            id = request.json["id"],
            image_id = request.json["image_id"],
            user_id=request.json["user_id"],
            meme_class = request.json["meme_class"],
            HS_class = request.json["HS_class"],
            text_class = request.json["text_class"],
            polarity_classA = request.json["polarity_classA"],
            polarity_classB = request.json["polarity_classB"],
            HS_strength = request.json["HS_strength"],
            HS_category = request.json["HS_category"],
            text_text = request.json["text_text"],
            text_language = request.json["text_language"]
        )

        try:
            db.session.add(new_imageannotation)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Imageannotation with id '{}' already exists".format(request.json["id"]))
        return Response(status=201, headers={"Location": url_for("api.imageannotationitem", id=request.json["id"])})


class ImageannotationItem(Resource):
    """
    Resource for ImageannotationItem. 
    Function GET gets one single imageannotation, PUT edits the imageannotation,
    and DELETE deletes the imageannotation.
    """

    def get(self, id):
        """
        GET method gets one single imageannotation
        """
        db_imageanno_id = ImageAnnotation.query.filter_by(id=id).first()
        if db_imageanno_id is None:
            return create_error_response(404, "Not found", "No imageannotation was found with id {}".format(id))

        body = HubBuilder(
            id = db_imageanno_id.id,
            image_id = db_imageanno_id.image_id,
            user_id = db_imageanno_id.user_id,
            meme_class = db_imageanno_id.meme_class,
            HS_class = db_imageanno_id.HS_class,
            text_class = db_imageanno_id.text_class,
            polarity_classA = db_imageanno_id.polarity_classA,
            polarity_classB = db_imageanno_id.polarity_classB,
            HS_strength = db_imageanno_id.HS_strength,
            HS_category = db_imageanno_id.HS_category,
            text_text = db_imageanno_id.text_text,
            text_language = db_imageanno_id.text_language
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.imageannotationitem", id=id))
        body.add_control("profile", IMAGEANNOTATION_PROFILE)
        body.add_control("collection", url_for("api.imageannotationcollection"))
        body.add_control_delete_imageannotation(id)
        body.add_control_edit_imageannotation(id)
        return Response(json.dumps(body), status=200, mimetype=MASON)


    def put(self, id):
        """
        PUT method edits one single imageannotation
        """
        db_imageanno_id = ImageAnnotation.query.filter_by(id=id).first()
        if db_imageanno_id is None:
            return create_error_response(404, "Not found", "No imageannotation was found with id {}".format(id))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.imageannotation_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_imageanno_id.id = request.json["id"],
        db_imageanno_id.photo_id = request.json["image_id"],
        db_imageanno_id.user_id=request.json["user_id"],
        db_imageanno_id.meme_class = request.json["meme_class"],
        db_imageanno_id.HS_class = request.json["HS_class"],
        db_imageanno_id.text_class = request.json["text_class"],
        db_imageanno_id.polarity_classA = request.json["polarity_classA"],
        db_imageanno_id.polarity_classB = request.json["polarity_classB"],
        db_imageanno_id.HS_strength = request.json["HS_strength"],
        db_imageanno_id.HS_category = request.json["HS_category"],
        db_imageanno_id.text_text = request.json["text_text"],
        db_imageanno_id.text_language = request.json["text_language"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Imageannotation with id '{}' already exists".format(request.json["id"]))
        return Response(status=204)


    def delete(self, id):
        """
        DELETE method deletes one single imageannotation
        """
        db_imageanno_id = ImageAnnotation.query.filter_by(id=id).first()
        if db_imageanno_id is None:
            return create_error_response(404, "Not found", "No imageannotation was found with id {}".format(id))

        db.session.delete(db_imageanno_id)
        db.session.commit()
        return Response(status=204)

