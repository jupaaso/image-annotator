# PWP SPRING 2021
# Image Annotator
# Group information
* Student 1. Merja Kreivi-Kauppinen   Merja.Kreivi-Kauppinen@student.oulu.fi
* Student 2. Juha Paaso               Juha.Paaso@student.oulu.fi

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

## Getting started
It is recommended to use virtual environment for using and testing the code. Usage of Python 3.7 or newer version is required. Use "pip install" to install virtual environment packages.

### Setting up virtual environment
Open command prompt (cmd) and proceed to C root folder. 
<li>   C:\> </li>

Then clone image-annotator project into your computer using following command. The command will create folder C:\image-annotator. 
<li>   C:\>git clone https://github.com/jupaaso/image-annotator.git
 
Proceed into image-annotator folder
<li>   C:\> cd image-annotator
<li>   C:\image-annotator> </code>
  
Next in your command prompt (cmd) create virtual environment on image-annotator folder. In the command prompt give following command: 
<li>  C:\image-annotator\python -m venv .venv </li>

Next activate created python virtual environment (on cmd):
<li>  C:\image-annotator>cd C:\ImageAnnotator\.venv\Scripts </li>
<li> 	C:\image-annotator\.venv\Scripts>activate.bat

You see the name of your virtual environment ".venv" in front of your command prompt now. Go back to image-annotator folder: (provide 'cd ..' on cmd twice)
<li>  (.venv) C:\image-annotator\.venv\Scripts>cd .. </li>
<li>	 (.venv) C:\image-annotator\.venv>cd .. </li>
<li>  (.venv) C:\image-annotator> </li>

### Installing required python libraries
Install the required libraries in your virtual environment in order to use this project code. Use following command in cmd:
<li>	 (.venv) C:\image-annotator>pip install -r requirements.txt

Install project with pip in editable (-e) mode with dot (.) 
<li>	 (.venv) C:\image-annotator>pip install -e .

There are many python libraries that is needed to be installed. The "requirements.txt" file on C:\image-annotator folder shows all those. These are all necessary to be installed in order ti use our code. 

## Running the tests
Some data is needed to be able to run the tests. Pytest is used to test both the database and resources. Pytest is already installed, as it is part of "requirements.txt" library list.

### Data
Data of memes and images was created by scraping Google image search with Beautiful Soup python library (https://pypi.org/project/beautifulsoup4/). Beautiful Soup library can be installed with ‘pip install beautifulsoup4’, if needed. Web scraping source code ‘WebScrapGoogle_images.py’ was used to collect raw data from web. Small test data folder ‘Data/ImageTest’ includes some original images scrapped from web. Private photographs were used to create ‘Data/PhotoTest’ -folder. ImageTest and PhotoTest are available at Data -folder.

### Flask settings
Set Flask configuration setting class as 'development' or 'production' or 'default' or 'testing'
<li>  (.venv) C:\image-annotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
<li>  (.venv) C:\image-annotator>set FLASK_APP=hub

### Database implementation
Init flask database basedir hub:
<li>  (.venv) C:\image-annotator>flask init-db

### Populating database
Populate flask database:
<li>	 (.venv) C:\image-annotator>flask populate-db

### Running database tests
In order to test the database "Flask settings" need to be completed. "Database implementation" and "Database population" is not needed for these tests. Details about the tests can be found at the comments inside db_test.py. 
Note! As there is another test file in this same folder, the resource_test.py, please rename that temporarily as "resource_test_.py so that only db_test.py file is run by pytest. Pytest command runs all files with file name starting or ending with test word.

Run the database tests inside "tests"-folder with following command:
<li>  (.venv) C:\image-annotator>cd tests>
<li>  (.venv) C:\image-annotator\tests>python -m pytest
<li>                                or alternatively python -m pytest -s
 
### Running resource tests
In order to test the resources "Flask settings" need to be completed. "Database implementation" and "Database population" is not needed for these tests. Details about the tests can be found at the comments inside resource_test.py

Run the resource tests inside "tests"-folder with following command:
<li>  (.venv) C:\image-annotator>cd tests>
<li>  (.venv) C:\image-annotator\tests>python -m pytest
<li>                                or alternatively python -m pytest -s

Note! As there is another test file in this same folder, the db_test.py, please rename that temporarily as "db_test_.py" so that only resource_test.py file is run by pytest. Pytest command runs all files with file name starting or ending with test word.

## Instruction how to use the provided client
We have prepared a small GUI for the image-annotator API. It runs on web-browser and it's based on HTML, CSS, JavaScript and jQuery. In order to use provided client "Flask settings", "Database implementation" and "Populating database" paragraph commands have to be completed. 

Next, run flask local host at http://localhost:5000/admin/ with following command in image-annotator folder:
<li>  (.venv) C:\image-annotator>flask run
 
Keep command prompt open, and open web-browser. Open http://localhost:5000/admin/ URL. This is your gate to image-annotator API. Wih help of the our client you can import images into database and annotate saved images, and keep all those saved and available in the database.

Open Image Annotator API at local host window by command:
<li>	 http://localhost:5000/admin/ 


### LOPPU ON IHAN TURHAA TÄLLÄ HETKELLÄ

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

