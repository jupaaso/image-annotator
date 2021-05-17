# PWP SPRING 2021
# Image Annotator
# Group information
* Student 1. Merja Kreivi-Kauppinen   Merja.Kreivi-Kauppinen@student.oulu.fi
* Student 2. Juha Paaso               Juha.Paaso@student.oulu.fi

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

## Getting started
It is recommended to use virtual environment for using and testing the code. Usage of Python 3.7 or newer version is required. Use "pip install" to install virtual environment packages.

### Setting up virtual environment
In order to create virtual environment, first create a folder in your computer where you want to install the virtual environment. For example on C:\ create ImageAnnotator folder

<li>   C:\ImageAnnotator>

Next in your command prompt (cmd) create virtual environment on ImageAnnotator folder. In the command prompt give following command (either one): 

<li>  C:\ImageAnnotator\python -m venv .venv </li>

Next activate created python virtual environment (on cmd):

<li>  C:\ImageAnnotator>cd C:\ImageAnnotator\.venv\Scripts </li>
<li> 	C:\ImageAnnotator\.venv\Scripts>activate.bat </li>
   
You see the name of your virtual environment ".venv" in front of your command prompt now. Go back to ImageAnnotator folder: (provide 'cd ..' on cmd twice)
    	(.venv) C:\ImageAnnotator>

### Installing project

Download, open and copy files of image-annotator-master ZIP folder (from GitHub) to ImageAnnotator folder.

Step into terminal command line and install necessary packages for the virtualenvironment using these commands:

<li>  pip install Flask</li>
<li>  pip install pysqlite3</li>
<li>  pip install flask_sqlalchemy</li>

### Installing required libraries
Note! When you later run the code, there may be need to install some other missing package. You can install missing packages with pip install command inside the same virtual environment terminal when (.venv) is at the beginning of the command line. 

Next check "launch.jason" file that it has right content. File is in sw_code folder. Correct location for this file in in ".vscode" folder.

### requirements.txt with dependencies
Image Annotator is created on python. The "requirements.txt" file is availabe from source_code folder.
Inside virtual environment there are following libraries
<li> click </li>
<li> Flask-SQLAlchemy </li>
<li> itsdangerous </li>
<li> Jinja2 </li>
<li> Markupsafe </li>
<li> SQLAlchemy </li>
<li> Werkzeug </li>

## Data
Data of memes and images was created by scraping Google image search with Beautiful Soup python library (https://pypi.org/project/beautifulsoup4/). Beautiful Soup library can be installed with ‘pip install beautifulsoup4’, if needed. Web scraping source code ‘WebScrapGoogle_images.py’ was used to collect raw data from web. Small test data folder ‘ImageTest’ includes some original images scrapped from web. Private photographs were used to create ‘PhotoTest’ -folder. ImageTest and PhotoTest are available at Data -folder.

## Database implementation
Populated database of Image Annotator can be created with test code ‘test_APIdb_populate4.py’. Example of created database ‘imageAnno_example1.db’ is available at Database -folder.

### Set up empty database
The ‘imageAnnoAPI.py’ -file includes all models of ‘imageAnno.db’ SQLite database. Database can be created in python virtual environment (defined above) for example by command – ‘python imageAnnoAPI.py’. Image Annotator database ‘imageAnno’ is created on the same path and folder with ‘imageAnnoAPI.py’ -file which creates the database. Size of created empty 'imageAnno.db' database is about 24 kt.

### Populating database
During development and testing phases database creation, population and query has been tested with a variety of testing codes. In order to populate database the "imageAnnoAPI.py" -file including database models, ImageTest and PhotoTest folders, and the population test code (for example ‘test_APIdb_populate4.py’) needs to be located in the same path and folder. 

The test code ‘test_APIdb_populate4.py’ creates and populates all database models of Image Annotator.

Activate python virtual environment before test code execution. Run the ‘test_APIdb_populate4.py’ with command  ‘python test_APIdb_populate4.py’. The test code will create the SQLite database and populate few instances into every data table with pre-set parameters. The test code copies images, image data, and ascii data into database. 

Database is created into project folder and named as "imageAnno.db". Database population test codes are available at ‘Database_test_code’ -folder:
<li> test_APIdb_populate1.py </li>
<li> test_APIdb_populate2.py </li>
<li> test_APIdb_populate3.py </li>
<li> test_APIdb_populate4.py </li>

## Testing during SW development phases
During API SW development cycles the code was tested with Visual Studio Code (VSC) debugger, Postman, and DB Browser.

VSC debugger utilized Python debugging support (Python extension for Visual Studio Code, GitHub homepage: https://github.com/Microsoft/vscode-python ), and required defined launch.json -file in order to function correctly. Utilized launch.json and settings.json -files are available at source_control -folder.

During API SW development steps Postman API Client (Google Chrome app) was used in testing to send REST Post request queries, and to read their responses within Postman. (Link to Postman website: https://www.postman.com/ )

DB Browser was used to check created and tested databases (DB Browser for SQLite, link to website: https://sqlitebrowser.org/ ). DB Browser provides possibility to execute for example simple integrity and foreign key checking. Created databases were check occasionally during API SW development steps.

## Database testing

... coming as soon as possible...

Run the codes defined below to test the database. Test codes are available at ‘Database_test_code’ -folder.
<li> test_APIdb_populate1.py </li>
<li> test_APIdb_populate2.py </li>
<li> test_APIdb_populate3.py </li>
<li> test_APIdb_populate4.py </li>
<li> test_APIdb_crudUser1.py </li>

