# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso
# Image Annotator - configurations
# config.py

import os

# ----------------------------------------------------------------------------------
# get file location, print file location if needed

basedir = os.path.abspath(os.path.dirname(__file__))
# print("\nconfig basedir:  ", basedir)

# -----------------------------------------------------------------------------------
# class Config implements an empty init_app() method

class Config:
    @staticmethod
    def init_app(app):
        pass

# ------------------------------------------------------------------------------------
# Config subclasses define settings for specific configurations
class DevelopmentConfig(Config):
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, "developmentAnno.db")
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestingConfig(Config):
    TESTING = True
    #DEBUG = False
    #SECRET_KEY="dev"    
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, "testingAnno.db")
    #SQLALCHEMY_TRACK_MODIFICATIONS=False

class ProductionConfig(Config):    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'MyPhotosAnno.db')


# config dictionary includes list of available configurations
config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}
