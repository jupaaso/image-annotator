# PWP SPRING 2021
# Image-Annotator
# Group information
* Student 1. Merja Kreivi-Kauppinen and email Merja.Kreivi-Kauppinen@student.oulu.fi
* Student 2. Juha Paaso             and email Juha.Paaso@student.oulu.fi

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

# Getting started
It is recommended to use virtual environment for using and testing the code. It is recommended to use VSCode.  Usage of Python 3.7 or newer version is required. Use "pip install" to install virtual environment packages.

# Setting up virtual environment
First, create a folder for this project on your computer, where you will install the virtual environment. 
Next start VSCode, and in VSCode open "File > Open Folder", open that folder.

Next open Python Terminal "Terminal > New Terminal". In the terminal give following command (either one): 

<li>  python -m venv .venv </li>
<li>  python -m venv /path/to/the/virtualenv (e.g. in Win10 "python -m D:\folder\venv") </li>
<li>  </li>    
You will see a dialog box opening "We noticed a new virtual environment has been created. Do you want to select it for the workspace folder?" and answer to that question "YES". 

Next on VSCodes bottom status bar, left side, there is text like "Python 3.7.4.64-bit". Press that test and select environment that was just created. Select environment "Python 3.7 (venv) ./venv/Scripts/python.exe" so that the text is changed into "Python 3.7.4.64-bit ('.venv')", text needs to end with the "('.venv'), as this venv is your virtual enviroment folder name in VSCode, and that can be seen in the VSCode Explorer view, on the left side. 

You also notice that in VSCode terminal the command line starts now with "(.venv)" text. Step into terminal command line and install necessary packages for the virtualenvironment using these commands:

<li>  pip install Flask</li>
<li>  pip install pysqlite3</li>
<li>  pip install flask_sqlalchemy</li>
<li>   </li>  

# Installing required libraries
Note! When you later run the code, there may be need to install some other missing package. You can install all missing packages now by using following command in the same virtual environment terminal when (.venv) is at the beginning of the command line. First copy requirements.txt into project folder and then give this command:
<li>  pip install -r requirements.txt

Next check "launch.jason" file that it has right content. File is in sw_code folder. Correct location for this file in in ".vscode" folder.

# requirements.txt with dependencies
Inside virtual environment there are following libraries
<li> click </li>
<li> Flask-SQLAlchemy </li>
<li> itsdangerous </li>
<li> Jinja2 </li>
<li> Markupsafe </li>
<li> SQLAlchemy </li>
<li> Werkzeug </li>

# Instruction how to populate the database
Place the file "test_API_dbPopulation.py" into your project folder. Run the codeline below and that will create three users into database's User-table. Then it finds all images loaded by User3 ("Meria Developer") and prints image information but not print the actual pictures.
<li>  python test_API_dbPopulation.py


The code repository must contain:
The ORM models and functions
A .sql dump of a database or the .db file (if you are using SQlite). You must provide a populated database in order to test your models.
The scripts used to generate your database (if any)
If you are using python, the requirements.txt file.
A README.md file containing:
All dependencies (external libraries) and how to install them
Define database (MySQL, SQLite, MariaDB, MongoDB...) and version utilized
Instructions how to setup the database framework and external libraries you might have used, or a link where it is clearly explained.
Instructions on how to setup and populate the database.
Instruction on how to run the tests of your database.
If you are using python a `requirements.txt` with the dependencies
NOTE: Your code MUST be clearly documented. Check Exercise 1 for examples on how to document the code.

In addition, it should be clear which is the code you have implemented yourself and which is the code that you have borrowed from other sources.
