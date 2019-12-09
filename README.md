# Movies - Data Mining Term Project Fall 2019
 
 It is basically a web based application developed for movies to search, classify text based on input query and also find a relevant images along with their captions.
 
 Link to PythonAnywhere : RavindraMeduri.pythonanywhere.com
 Dataset Link : https://www.kaggle.com/rounakbanik/the-movies-dataset
 
 Phase1: Movie Search 

 Search feature ranks the result based on TF - IDF scores
 Input: Any free form text
 Output: shows list of movies along with description that matches keywords provided as Input and calculates TF and IDF scores
 
 Link to Phase 1 report:
 https://ravindrameduri.wixsite.com/portfolio/post/manage-your-blog-from-your-live-site
 
 Link to Phase 1 Demo:
 http://ravindrameduri.pythonanywhere.com/search
 
 Phase2: Movie Classifier
 Input: Any free form text
 Output: shows list of genres based on input query
 
 Link to Phase 2 report:
 https://ravindrameduri.wixsite.com/portfolio/post/design-a-stunning-blog
 
 Link to Phase 2 Demo:
 http://ravindrameduri.pythonanywhere.com/search
 
 Phase3: Movie Image Captioning
 Input: Any free form text
 Output: shows list of images along with caption based on input query
 
 Link to Phase 3 report:
 https://ravindrameduri.wixsite.com/portfolio/post/grow-your-blog-community
 
 Link to Phase 3 Demo:
 http://ravindrameduri.pythonanywhere.com/search
 
 
 How to Deploy code:
 
1.Setup on PythonAnywhere
2.Create an account on PythonAnywhere
3.Open up a bash console
4.Install all libraries which are dependent to run the application
5.Type in the console git init
6.Type in the console git clone https://github.com/RavindraMeduri/Movies.git
7.Exit the terminal, and go to the "Web" tab to create a new web app
8.change the virtualenv to /home/RavindraMeduri/.virtualenvs/flaskapp
9.Create a "Manual" web app (not "Flask" webapp) with Python 3.7
10.Set "Source code" and "Working directory" to be /home/yourname/
11.Open the WSGI configuration file,uncomment the relevant parts under the heading "Flask". Change the last line to from app import app as application, as currently the name of our main file is app.py
12.Reload the web app, and it should be available at https://yourname.pythonanywhere.com

Setup on localhost:

Create a repository using github desktop
set the path to github and keep all the project files inside the repository
publish the repository

