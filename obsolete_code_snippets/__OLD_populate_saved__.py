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

