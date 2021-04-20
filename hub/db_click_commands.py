import os
import glob
import base64
from io import BytesIO

from datetime import datetime
import click
from flask.cli import with_appcontext
from hub import db
from hub.constants import *
from hub import models
#start ----------------------------------------------------------------------------
# run this after set FLASK_ENV=development (or testing)
# set FLASk_APP=hub
# flask init-db
@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()

# after running init-db (above)
# run this by 
#flask populate-db
@click.command("populate-db")
@with_appcontext
def generate_test_data():
    import datetime
    import random        
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    upload = ""
    try:
        upload = basedir + UPLOAD_FOLDER        
        if not os.path.exists(upload):
            os.makedirs(upload)
    except OSError as e:
        print('FAILED : ' + str(upload), file=sys.stderr)

    user1 = User(user_name = "Meria Developer", user_password="mötkäle")
    user2 = User(user_name = "Juha Engineer", user_password="auty8f645bf")
    user3 = User(user_name = "Matti Meikäläinen", user_password="1234567890")
    user4 = User(user_name = "Katti ole' Matikainen", user_password="åäöpolkijju876")
    user5 = User(user_name = "Hessu Hopo :-) ", user_password="K8Hyf43HVruj47")
    #user6 = User(user_name = "Juha Engineer", user_password="vl75dJrVh90765d")

    # Add model to the session
    db.session.add_all([user1, user2, user3, user4, user5])

    # Save session to database with commit
    db.session.commit()

    # Collect defined user from database
    userqueried = User.query.filter_by(user_name="Meria Developer").first()

# Add images of image_list (collected from defined folder in path) for user in database
# and commit to database
    image_list = getImageData(upload)
    for im in image_list:
        image = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], publish_date=im["publish_date"], location=im["location"], is_private=im["is_private"], date=im["date"])
        print(image.publish_date)
        print(image.date)
        userqueried.image_user.append(image)
        db.session.commit()

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

# Collect defined user from database
    userqueried = User.query.filter_by(user_name="Matti Meikäläinen").first()

# Add photos of photo_list (collected from defined folder in path) for user in database
# and commit to database
    photo_list = getPhotoData(upload)
    for im in photo_list:
#        photo = PhotoContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"])
        photo = ImageContent(data=im["data"], ascii_data=im["ascii_data"], name=im["name"], date=im["date"], location=im["location"], is_private=True)
        userqueried.photo_user.append(photo)
        db.session.commit()

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

#####################################################        

# Collect images and image data from defined ImageTest -folder to image_list
def getImageData(upload):
    image_list = []
    source_images_folder = "C:\\PWBproject\\ImageAnnotator\\data\\ImageTest\\"
    for filename in glob.glob(source_images_folder + '*.jpg'):
        print("Filename:  ", filename)
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
                "location": save_to_upload(upload, source_images_folder, os.path.basename(filename)),
                "is_private": False,
                "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
        image_list.append(thisdict)
    return image_list

def save_to_upload(target_folder, source_folder, source_filename):
     # collect the filename
    from shutil import copy        
    
    full_path = os.path.join(source_folder, source_filename)
            
    # copy file from source location to target location
    copy(full_path, target_folder) 
    return str(os.path.join(UPLOAD_FOLDER, source_filename))

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

# Collect photos and photo data from defined PhotoTest -folder to photo_list
def getPhotoData(upload):
    from PIL import Image, ExifTags

    photo_list = []
    source_photos_folder = 'C:\PWBproject\ImageAnnotator\data\PhotoTest/'
    for filename in glob.glob(source_photos_folder + '*.jpg'):
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
                "location":save_to_upload(upload, source_photos_folder, os.path.basename(filename))
            }
        photo_list.append(thisdict)
    return photo_list

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
