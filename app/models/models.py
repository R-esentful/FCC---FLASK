"""
RE STRUCTURING OUR APPLICATION : MODELS (DATABASE QUERYING)
"""
# Referenced from the APP/__init__.py  and import the variable "DB","BCRYPT"
from app import db,bcrypt

"""
Create Model for querying. Always refer db.Model for database querying.

db.Column(creating Column for database)
db.String(set value to string, we can also set length)
db.Integer(set value to integer)

Parameters:
    primary_key = sets the column to be primary key
    Length = sets the length of string (Only applicable to db.String() )
    Unique = sets the value to unique (Should have no same value)
    Nullable = sets the value nullable (should not be null)

TO CREATE DATABASE:
    1. Go to terminal and type flask shell.
    2. type db.create_all()

"""

# USER Schema
class User(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    username = db.Column(db.String(length = 30),unique = True,nullable = False)
    email_address = db.Column(db.String(length = 50),unique = True,nullable = False)
    password_hash = db.Column(db.String(length = 60),nullable = False)
    budget = db.Column(db.Integer(),nullable = False,default = 1000)

    # One to Many Relationship
    items = db.relationship('Items',backref = 'owned_user',lazy= True)

    # @property are the getters, setters and deleters
    # create an instance in which we could use it for our routes
    # this specific property is a "GETTER"
    @property
    def password(self):
        return self.password

    # creates a password setter for our instance
    # this specific property is a "SETTER"
    @password.setter
    # function for setting password.
    def password(self,plain_text_password):
        # creates a hashed password using a specific hashing algorithm which is bcrypt 
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

# ITEMS Schema
class Items(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(length = 30),unique = True,nullable = False)
    price = db.Column(db.Integer(),nullable = False)
    barcode = db.Column(db.String(length = 12),unique = True,nullable = False)
    description = db.Column(db.String(length = 1024),unique = True,nullable = False)

    # Sets the foreign key to user ID
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))

    # Reference the item to return in the database when querying. e.g Item 1 name = Phone
    # It will return Item Phone 
    def __repr__(self):
        return f'Item {self.name}'