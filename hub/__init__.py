# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso
# Image Annotator - initialize code package
# __init__.py

# the code needs two more library packages
# pip install Flask-Script
# pip install Flask-Migrate

# in order to start development server on windows
#(.venv) C:\PWBproject\ImageAnnotator\hub>set FLASK_APP=hub
#(.venv) C:\PWBproject\ImageAnnotator\hub>set FLASK_ENV=development

import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
# start
from hub.constants import *
#from config import config
# end


# -----------------------------------------------------------------
# initialize database with SQAlchemy
db = SQLAlchemy()

# get file location, print file location if needed
basedir = os.path.abspath(os.path.dirname(__file__))
print("\ninit basedir:  ", basedir)

# -----------------------------------------------------------------
# create app with Flask, get defined configuration from config file
# initialize configuration with init_app()
# initialize app with init_app()

#def create_app(config_name):
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    # start
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
    # filen tallennukseen tarvitaan nämä
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # disable cache
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # end file

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        app.config['DEBUG'] = True

    try:
        os.makedirs(app.instance_path)        
    except OSError:        
        pass

    try:
        upload = basedir + UPLOAD_FOLDER        
        if not os.path.exists(upload):
            os.makedirs(upload)
    except OSError as e:
        print('FAILED : ' + str(upload), file=sys.stderr)
    db.init_app(app)
    
    from . import models
    from . import api_routes

    app.cli.add_command(models.init_db_command)
    app.register_blueprint(api_routes.api_bp)

    return app

"""
    @app.route(LINK_RELATIONS_URL)
    def send_link_relations():
        return "link relations"

    @app.route("/profiles/<profile>/")
    def send_profile(profile):
        return "you requests {} profile".format(profile)

    @app.route("/admin/")
    def admin_site():
        return app.send_static_file("html/admin.html")
"""
    # attach routes and custom error pages here
    #print("instance path : ", app.instance_path)

    # end

    
