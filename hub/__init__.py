# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# Image Annotator API __init__.py

# This file initializes flask app

# ------------------------------------------------------------------------------------------
# The code package of Image Annotator API needs following library packages

# pip install Flask
# pip install pysqlite3
# pip install Flask-sqlalchemy
# pip install flask-restful

# pip install pytest
# pip install pytest-cov

# pip install Flask-Script
# pip install Flask-Migrate

# pip install Pillow
# pip install jsonschema

# pip install requests

# -------------------------------------------------------------------------------------------
"""
In order run ImageAnnotator flask API and this file 
activate virtual environment, set flask, init database and populate database.

Activate created python virtual environment (on cmd):
    cd C:\PWPproject\ImageAnnotator\.venv\Scripts
    activate.bat

Go to ImageAnnotator folder: (provide 'cd ..' on cmd)
    (.venv) C:\PWPproject\ImageAnnotator>

Set cofiguration setting class as 'development' or 'production' or 'default' or 'testing'
    (.venv) C:\PWPproject\ImageAnnotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\PWPproject\ImageAnnotator\extracodes>set FLASK_APP=hub

Init flask database basedir hub:
    (.venv) C:\PWPproject\ImageAnnotator>flask init-db

Populate flask database:
    (.venv) C:\PWPproject\ImageAnnotator>flask populate-db

Run flask local host at http://localhost:5000/admin/

    (.venv) C:\PWPproject\ImageAnnotator>flask run

This code creates database models, 
and populates User, PhotoContent, PhotoAnnotation, ImageContent and ImageAnnotation models
"""
# -------------------------------------------------------------------------------------------

import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from hub.constants import *
# from config import config

# -----------------------------------------------------------------
# initialize database with SQAlchemy
db = SQLAlchemy()

# get file location, print file location if needed
basedir = os.path.abspath(os.path.dirname(__file__))
print("\nPrint of init file : init basedir :  ", basedir)

# -----------------------------------------------------------------
# create app with Flask, get defined configuration from config file
# initialize configuration with init_app()
# initialize app with init_app()

# def create_app(config_name):
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    #app.config.from_object(config[config_name])
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///development.db"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + "../" + "developmentAnno.db"
    #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #config[config_name].init_app(app)
    #db = SQLAlchemy(app)
    
    app.config.from_mapping(
        SECRET_KEY="dev",
        #SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "developmentTEST.db"),
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join("..//", "developmentAnno.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # following definitions are needed in order to save image / photo files
    app.config['UPLOAD_FOLDER_PHOTOS'] = UPLOAD_FOLDER_PHOTOS
    app.config['UPLOAD_FOLDER_IMAGES'] = UPLOAD_FOLDER_IMAGES
    
    # disable cache
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    
    # do not use rows below if not necessary ------------------------------------
    else:
        app.config.from_mapping(test_config)
        #app.config['DEBUG'] = True
    # ---------------------------------------------------------------------------
    
    try:
        os.makedirs(app.instance_path)        
    except OSError:        
        pass
    
    # initialize flask app
    db.init_app(app)
    
    from . import models
    from . import api_routes

    # create images and photos folders to static folder with helper function in models file
    models.create_static_folders()
    
    # init database
    app.cli.add_command(models.init_db_command)
    
    # populate database - generate test data
    app.cli.add_command(models.generate_test_data)

    # set blueprint
    app.register_blueprint(api_routes.api_bp)

    # flask app routes defined here ----------------------------------------
    # routes not defined in api_routes because of some coding challenges

    @app.route(LINK_RELATIONS_URL)
    def send_link_relations():
        return "link relations"

    @app.route("/admin/")
    def admin_site():
        return app.send_static_file("html/admin.html")

    @app.route("/profiles/<profile>/")
    def send_profile(profile):
        return "you requests {} profile".format(profile)

    return app

    # attach routes and custom error pages here
    #print("instance path : ", app.instance_path)