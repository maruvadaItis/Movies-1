# Movies - Data Mining Term Project Fall 2019
 Movie Search
 
 Link to PythonAnywhere
 RavindraMeduri.pythonanywhere.com
 
 
1.Setup on PythonAnywhere
2.Create an account on PythonAnywhere
3.Open up a bash console
4.Type in mkvirtualenv and name the environment as "flaskapp" including python version
5.Install all libraries which are dependent to run the application
6.Type in the console git init
7.Type in the console git clone https://github.com/RavindraMeduri/Movies.git
8.Exit the terminal, and go to the "Web" tab to create a new web app
9.change the virtualenv to /home/RavindraMeduri/.virtualenvs/flaskapp
10.Create a "Manual" web app (not "Flask" webapp) with Python 3.7
11.Set "Source code" and "Working directory" to be /home/yourname/
12.Open the WSGI configuration file,uncomment the relevant parts under the heading "Flask". Change the last line to from app import app as application, as currently the name of our main file is app.py
13.Reload the web app, and it should be available at https://yourname.pythonanywhere.com

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
