# pythontest

IDE: PyCharm Community Edition 2019.3.4 x64
Python 3.8.2


This is project is used to test my developer skills using Flask for developing a  web application should suggest articles fetched from an RSS feed. Suggestions are made based on keywords submitted by the user. Each user configures their own list of keywords.

This project uses the modules contained in the requirements.txt file, along with their versions which you can use to install them in to your venv before running this project.

The project structure is one main module called run.py, which only has one responsibility - running the code, and the other modules like routes, forms, models, html etc are inside the pythontest package. Routes contains all the routes which are accesable thru the views, forms contain all the forms that are used to input the data and into the database, models is where the database is created using SQLAlchemy. The templates folder holds all the views (.html) files which are extending the layout.htmlm and use bootstrap and some css for styling.

We can run our app by running python run.py in our Command Line.

Testing was done frequently during developement and afterwards.

## Installation

-Make a new venv and install the requirements.txt file given with the project 'pip install -r requirements.txt'
-run the code using python run.py
-go to browser and view it on localhost:5000
