# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso

# Image Annotator API - api_routes.py
# ------------------------------------------------------------------------

from flask import Blueprint
from flask_restful import Api

# import hub.resources
from hub.resources import UserItem, UserCollection, UserLogin
from hub.resources import PhotoItem, PhotoCollection, ImageItem, ImageCollection
from hub.resources import PhotoannotationItem, PhotoannotationCollection, ImageannotationItem, ImageannotationCollection

# -----------------------------------------------------------
# define api blueprint prefix

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# -----------------------------------------------------------
# define and add resources to api

api.add_resource(UserLogin, "/userlogin/")

api.add_resource(UserCollection, "/users/")
api.add_resource(UserItem, "/users/<user_name>/")

api.add_resource(PhotoCollection, "/photos/")
api.add_resource(PhotoItem, "/photos/<id>/")

api.add_resource(ImageCollection, "/images/")
api.add_resource(ImageItem, "/images/<id>/")

api.add_resource(PhotoannotationCollection, "/photoannotations/")
api.add_resource(PhotoannotationItem, "/photoannotations/<id>/")

api.add_resource(ImageannotationCollection, "/imageannotations/")
api.add_resource(ImageannotationItem, "/imageannotations/<id>/")

# ----------------------------------------------------------
# define routes

"""
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""
# new start
"""
@app.route("/api/")
def entry_point():
    
    body = MasonBuilder()
    body.add_namespace("annometa", "/api/")
    body.add_control("annometa:users-all", "/api/users/")
    return Response(json.dumps(body), mimetype=MASON)

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
# 
# --------------------------------------------------------------