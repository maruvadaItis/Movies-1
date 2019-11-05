# Movies - Data Mining Term Project Fall 2019
 Movie Search
 
 Link to PythonAnywhere
 RavindraMeduri.pythonanywhere.com
 
 
Setup on PythonAnywhere
Create an account on PythonAnywhere
Open up a bash console
Type in mkvirtualenv and name the environment as "flaskapp" including python version
Install all libraries which are dependent to run the application
Type in the console git init
Type in the console git clone https://github.com/RavindraMeduri/Movies.git
Exit the terminal, and go to the "Web" tab to create a new web app
change the virtualenv to /home/RavindraMeduri/.virtualenvs/flaskapp
Create a "Manual" web app (not "Flask" webapp) with Python 3.7
Set "Source code" and "Working directory" to be /home/yourname/
Open the WSGI configuration file,uncomment the relevant parts under the heading "Flask". Change the last line to from app import app as application, as currently the name of our main file is app.py
Reload the web app, and it should be available at https://yourname.pythonanywhere.com

Setup on localhost
//Create a repository using github desktop
//set the path to github and keep all the project files inside the repository
//publish the repository

Open up a bash console
Type in git clone https://github.com/RavindraMeduri/Movies.git
Enter the repository cd Data_Mining_Project
Install the required packages pip install -r requirements.txt
Run the app python app.py
The application should be available on localhost at the default Flask port 127.0.0.1:5000
