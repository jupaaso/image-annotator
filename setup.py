# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen and Juha Paaso
# Image Annotator API - setup.py

# In order to run tests project need to be installed so that it can be found from the virtual environment's path
# Python packages are installed with setup script

# package name = hub
# package version = 0.1.0

# packages=find_packages()
# include_package_data = True
# To include package data - as static files: HTML, CSS, JS, JSON schemas, pictures etc. that are in static folder. 
# In order for them to be included they also need to be listed in a file called MANIFEST.in.

from setuptools import find_packages, setup

setup(
    name="hub",
    version="0.1.0",
    author="Merja Kreivi-Kauppinen and Juha Paaso",
    url="https://github.com/jupaaso/image-annotator",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-restful",
        "flask-sqlalchemy",
        "SQLAlchemy",
        "pysqlite3",
        "pytest",
        "pytest-cov",
        "Flask-Script",
        "Flask-Migrate",
        "Pillow",
        "jsonschema",
        "requests",
        "click",
        "itsdangerous",
        "Jinja2",
        "Markupsafe",
        "Werkzeug"
    ]
)