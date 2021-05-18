# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# Image Annotator API - utils.py

# This file defines Mason builder classes

# ------------------------------------------------------------------------

import json
import base64
import glob
from io import BytesIO
from datetime import datetime
from shutil import copy
from PIL import Image, ExifTags
from flask import Response, request, url_for

#import hub.api_routes
from hub.constants import *
#import hub.models
from hub.models import *

# define Mason Builder Class ------------------------------------------------------

class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). 
        However we are being lazy and supporting just one message.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. 
        A namespace defines where our link relations are coming from. 
        The URI can be an address where
        developers can find information about our link relations.
        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. 
        Technically only certain properties are allowed for kwargs 
        but we're being lazy and don't perform any checking.
        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href


# -------------------------------------------------------------------------------------------------
# Define hub builder class and create hub builder with MasonBuilder

class HubBuilder(MasonBuilder):

    ##### user --------------------------------------------------

    @staticmethod
    def user_schema():
        schema = {
            "type": "object",
            "required": ["user_name", "user_password"]
        }
        props = schema["properties"] = {}
        props ["user_name"] = {
            "description": "Name of the user",
            "type": "string"
        }
        props ["user_password"] = {
            "description": "Password of the user",
            "type": "string"
        }
        return schema

    def add_control_add_user(self):
        """
        Control to add user
        """
        self.add_control(
            "annometa:add-user",
            url_for("api.usercollection"),
            method="POST",
            encoding="json",
            title="Add new user",
            schema=self.user_schema()
        )
    
    def add_control_delete_user(self, user_name):
        """
        Control to delete user
        """
        self.add_control(
            "annometa:delete",
            url_for("api.useritem", user_name=user_name),
            method="DELETE",
            title="Delete user"
        )

    def add_control_edit_user(self, user_name):
        """
        Control to edit user
        """
        self.add_control(
            "edit",
            url_for("api.useritem", user_name=user_name),
            method="PUT",
            encoding="json",
            title="Edit user",
            schema=self.user_schema()
        )

    ##### login -----------------------------------------------------
    
    def add_control_login_user(self):
        """
        Control to login user
        """
        self.add_control(
            "annometa:login",
            url_for("api.userlogin"),
            method="POST",
            encoding="json",
            title="Login user",
            schema=self.user_schema()
        )

    ##### photo -----------------------------------------------------

    @staticmethod
    def photo_schema():
        schema = {
            "type": "object",
            "required": ["name", "publish_date", "location", "is_private", "date"]
        }
        props = schema["properties"] = {}
        props ["name"] = {
            "description": "Name of photograph",
            "type": "string"
        }
        props ["publish_date"] = {
            "description": "Date (metadata) when photograph was taken or created, , if available",
            "type": "string",
            "pattern": "^[0-9]{4}-[01][0-9]-[0-3][0-9]T[0-9]{2}:[0-5][0-9]:[0-5][0-9]Z$"
        }
        props ["location"] = {
            "description": "Location of loaded photograph file in server",
            "type": "string"
        }
        props ["is_private"] = {
            "description": "Privacy class of photograph",
            "type": "boolean"
        }
        props ["date"] = {
            "description": "Photograph loading timestamp",
            "type": "string",
            "pattern": "^[0-9]{4}-[01][0-9]-[0-3][0-9]T[0-9]{2}:[0-5][0-9]:[0-5][0-9]Z$"
        }
        return schema

    def add_control_add_photo(self):
        self.add_control(
            "annometa:add-photo",
            url_for("api.photocollection"),
            method="POST",
            encoding="json",
            title="Add a new photo to photo collection",
            schema=self.photo_schema()
        )

    def add_control_delete_photo(self, id):
        self.add_control(
            "annometa:delete",
            url_for("api.photoitem", id=id),
            method="DELETE",
            title="Delete this photo"
        )

    def add_control_edit_photo(self, id):
        self.add_control(
            "annometa:edit",
            url_for("api.photoitem", id=id),
            method="PUT",
            encoding="json",
            title="Edit this photo",
            schema=self.photo_schema()
            )

    def add_control_get_photo(self, id):
        self.add_control(
            "annometa:photo",
            url_for("api.photoitem", id=id),
            method="GET",
            encoding="json",
            title="Add control to get photo",
            schema=self.photo_schema()
            )

    def add_control_all_photos(self):
        self.add_control(
            "annometa:photos",
            "/api/photos/",
            method="GET",
            encoding="json",
            title="Add control to get all photos",
            schema=self.photo_schema()
            )

    ##### image -----------------------------------------------------

    @staticmethod
    def image_schema():
        schema = {
            "type": "object",
            "required": ["name", "publish_date", "location", "is_private", "date"]
        }
        props = schema["properties"] = {}
        props ["name"] = {
            "description": "Name of image",
            "type": "string"
        }
        props ["publish_date"] = {
            "description": "Date (metadata) when image was taken or created, if available",
            "type": "string",
            "pattern": "^[0-9]{4}-[01][0-9]-[0-3][0-9]T[0-9]{2}:[0-5][0-9]:[0-5][0-9]Z$"
        }
        props ["location"] = {
            "description": "Original location of loaded image file",
            "type": "string"
        }
        props ["is_private"] = {
            "description": "Privacy class of image",
            "type": "boolean"
        }
        props ["date"] = {
            "description": "Image loading timestamp",
            "type": "string",
            "pattern": "^[0-9]{4}-[01][0-9]-[0-3][0-9]T[0-9]{2}:[0-5][0-9]:[0-5][0-9]Z$"
        }
        return schema

    def add_control_add_image(self):
        self.add_control(
            "annometa:add-image",
            url_for("api.imagecollection"),
            method="POST",
            encoding="json",
            title="Add a new image to image collection",
            schema=self.image_schema()
        )

    def add_control_delete_image(self, id):
        self.add_control(
            "annometa:delete",
            url_for("api.imageitem", id=id),
            method="DELETE",
            title="Delete this image"
        )
    
    def add_control_edit_image(self, id):
        self.add_control(
            "annometa:edit",
            url_for("api.imageitem", id=id),
            method="PUT",
            encoding="json",
            title="Edit this image",
            schema=self.image_schema()
        )    

    def add_control_get_image(self, id):
        self.add_control(
            "annometa:image",
            "/api/images/image/",
            url_for("api.imageitem", id=id),
            method="GET",
            encoding="json",
            title="Add control to get image",
            schema=self.image_schema()
            )

    def add_control_all_images(self):
        self.add_control(
            "annometa:images",
            "/api/images/",
            method="GET",
            encoding="json",
            title="Add control to get all images",
            schema=self.image_schema()
            )

    ##### photoannotation -----------------------------------------------------

    @staticmethod
    def photoannotation_schema():
        schema = {
            "type": "object",
            "required": ["persons_class", "slideshow_class", "positivity_class",
            "text_free_comment", "text_persons", "text_persons_comment"] 
        }
        props = schema["properties"] = {}
        props ["persons_class"] = {
            "description": "Classifier to define if photo includes persons",
            "type": "boolean"
        }
        props ["slideshow_class"] = {
            "description": "Classifier to define if photo is used in slideshow",
            "type": "boolean"
        }
        props ["positivity_class"] = {
            "description": "Classifier to define how good photo is",
            "type": "number"
        }
        props ["text_free_comment"] = {
            "description": "Free comment of photo",
            "type": "string"
        }
        props ["text_persons"] = {
            "description": "Persons of photo",
            "type": "string"
        }
        props ["text_persons_comment"] = {
            "description": "Free comment of persons on photo",
            "type": "string"
        }
        return schema

    def add_control_add_photoannotation(self):
        self.add_control(
            "annometa:add-photoannotation",
            url_for("api.photoannotationcollection"),
            method="POST",
            encoding="json",
            title="Add new photoannotation to photoannotation collection",
            schema=self.photoannotation_schema()
        )

    def add_control_delete_photoannotation(self, id):
        self.add_control(
            "annometa:delete",
            url_for("api.photoannotationitem", id=id),
            method="DELETE",
            title="Delete photoannotation"
        )

    def add_control_edit_photoannotation(self, id):
        self.add_control(
            "edit",
            url_for("api.photoannotationitem", id=id),
            method="PUT",
            encoding="json",
            title="Edit photoannotation",
            schema=self.photoannotation_schema()
        )

    def add_control_get_photoannotation(self, id):
        self.add_control(
            "annometa:photoannotation",
            "/api/photoannotations/photoannotation/",
            url_for("api.photoannotationitem", id=id),
            method="GET",
            encoding="json",
            title="Add control to get this photoannotation",
            schema=self.photoannotation_schema()
            )

    def add_control_all_photoannotations(self):
        self.add_control(
            "annometa:photoannotations",
            "/api/photoannotations/",
            method="GET",
            encoding="json",
            title="Add control to get all photoannotations",
            schema=self.photoannotation_schema()
            )

##### imageannotation -----------------------------------------------------

    @staticmethod
    def imageannotation_schema():
        schema = {
            "type": "object",
            "required": ["meme_class", "HS_class", "text_class", 
            "polarity_classA", "polarity_classB",
            "HS_strength", "HS_category", "text_text", "text_language"]
        }
        props = schema["properties"] = {}
        props ["meme_class"] = {
            "description": "Classifier to define if image is meme",
            "type": "boolean"
        }
        props ["HS_class"] = {
            "description": "Classifier to define if image is hate speech",
            "type": "boolean"
        }
        props ["text_class"] = {
            "description": "Classifier to define if image includes text",
            "type": "boolean"
        }
        props ["polarity_classA"] = {
            "description": "Classifier to define polarity value for image",
            "type": "number"
        }
        props ["polarity_classB"] = {
            "description": "Classifier to define polarity value for image",
            "type": "number"
        }
        props ["HS_strength"] = {
            "description": "Classifier to define hate speech strength value for image",
            "type": "number"
        }
        props ["HS_category"] = {
            "description": "Hate speech category classifier for image",
            "type": "string"
        }
        props ["text_text"] = {
            "description": "Text on image",
            "type": "string"
        }
        props ["text_language"] = {
            "description": "Language category of text on photo",
            "type": "string"
        }
        return schema

    def add_control_add_imageannotation(self):
        self.add_control(
            "annometa:add-imageannotation",
            url_for("api.imageannotationcollection"),
            method="POST",
            encoding="json",
            title="Add new annotation to imageannotation collection",
            schema=self.imageannotation_schema()
        )

    def add_control_delete_imageannotation(self, id):
        self.add_control(
            "annometa:delete",
            url_for("api.imageannotationitem", id=id),
            method="DELETE",
            title="Delete imageannotation"
        )

    def add_control_edit_imageannotation(self, id):
        self.add_control(
            "edit",
            url_for("api.imageannotationitem", id=id),
            method="PUT",
            encoding="json",
            title="Edit imageannotation",
            schema=self.imageannotation_schema()
        )

    def add_control_get_imageannotation(self, id):
        self.add_control(
            "annometa:imageannotation",
            "/api/imageannotations/imageannotation/",
            url_for("api.imageannotationitem", id=id),
            method="GET",
            encoding="json",
            title="Add control to get this imageannotation",
            schema=self.imageannotation_schema()
            )

    def add_control_all_imageannotations(self):
        self.add_control(
            "annometa:imageannotations",
            "/api/imageannotations/",
            method="GET",
            encoding="json",
            title="Add control to get all imageannotations",
            schema=self.imageannotation_schema()
            )


# Define error response function ---------------------------------------------------

def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)


# ----------------------------------------------------------------------------------
# Helper functions for image/photo files handling 

# Helper function to set meta data to dict data
# this function can be / will be used when populating data for code development purposis of resources
# and testing resources

def set_photo_meta_data_to_dict(filename, is_private):
    # default publish_date is None - beacuse it is none for social media images    
    publish_date = None
    # get exifdata only from private photo items
    if is_private:
        imageFile = Image.open(filename)
        exifdata = imageFile.getexif()
        if exifdata:
            # Make a map with exifdata tag names
            exif = { ExifTags.TAGS[k]: v for k, v in exifdata.items() if k in ExifTags.TAGS and type(v) is not bytes }                
            # Grab the date
            try:
                publish_date = datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
            except Exception as e:
                print('Print 1 of utils -file: Unable to get DateTimeOriginal from exif for %s' % filename)
                timestamp = os.path.getctime(filename)
                publish_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            print('Print 2 of utils -file: Unable to get date from exif for %s' % filename)        
        del imageFile
    else:
        timestamp = os.path.getctime(filename)
        publish_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    # below location is set empty ("") since it should be defined by calling function
    thisdict = {
        "name": os.path.basename(filename),
        "publish_date": datetime.fromisoformat(publish_date),            
        "is_private": is_private,
        "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "location" : "" 
    }
    return thisdict


def convert_image_to_db_object(location, name, is_private):    
    return ImageContent(
        name = name,
        location = location,
        date = datetime.now(),
        is_private=is_private            
    )        


# from https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
