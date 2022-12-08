"""
RESTRUCTURED : SAVE THIS ON THE __INIT__.PY FILE this is to create a python package that
               will be used to on to reference this specific directory as a package. 

NOTE: THIS IS TO PREVENT CIRCULAR IMPORTS


Initilialize flask application by importing flask module

Flask(for the main application),render_template (for rendering)
SQLAlchemy(database)
Flask Bcrypt ( for password hashing in saving to database )

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# Initialize application
app = Flask(__name__)



"""
# Sets the Application database to be use
# I'll be using MYSQL for my Database (Always install PYMYSQL , mysql-connector,mysql-connector-python if you are using MYSQL DB!)
# MYSQL STRUCTURE: 'mysql://your_username:your_password@localhost/database_name'

"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fcc_flaskdb'
# Set SECRET KEY for our flask application. This is for the security of our application and for us to use the flask forms.
app.config['SECRET_KEY'] = '7a7c78a19d7175a0b0d01f2d2d7bbf0e'

# Initialize database and reference it to the application
db = SQLAlchemy(app)

# Initialize bcrypt and reference it to the application
# CASE SENSITIVE!
bcrypt = Bcrypt(app)


# 
from app import routes