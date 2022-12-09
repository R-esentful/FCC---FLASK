"""
RE STRUCTURING OUR APPLICATION : MODELS (DATABASE QUERYING)
"""
# Referenced from the APP/__init__.py  and import the variable "DB","BCRYPT","LOGIN_MANAGER"
from app import db,bcrypt,login_manager
# Flask login UserMixin which adds properties for logging in such as 
# is_authenticated,is_active,is_anonymous and etc.
from flask_login import UserMixin
"""
Create Model for querying. Always inherit "db.Model" for database querying and "UserMixin" for authentication.

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


# You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the str ID of a user, and return the corresponding user object.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# USER Schema
class User(db.Model,UserMixin):
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

    # create an instance for our password
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
    
    # function that checks the password
    def check_password(self,attempted_password):
        # compares both the paremeters of password hash and the attempted password
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    # Create an instance to modify our budget
    @property
    def prettier_budget(self):
        if(len(str(self.budget))) >=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'

    # function that checks if the user has sufficient balance
    def can_purchase(self,item_obj):
        return self.budget >= item_obj.price

    # function that checks if the user owns the item
    def can_sell(self,item_obj):
        return item_obj in self.items
# ITEMS Schema
class Items(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(length = 30),unique = True,nullable = False)
    price = db.Column(db.Integer(),nullable = False)
    barcode = db.Column(db.String(length = 12),unique = True,nullable = False)
    description = db.Column(db.String(length = 1024),unique = True,nullable = False)

    # Sets the foreign key to user ID
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))

    # Function to assign ownership to the item.
    def assign_item(self,user):
       self.owner = user.id
       user.budget -= self.price
       db.session.commit()

    # Function to sell the item
    def sell_item(self,user):
        self.owner = None;
        user.budget += self.price
        db.session.commit()


    # Reference the item to return in the database when querying. e.g Item 1 name = Phone
    # It will return Item Phone 
    
    def __repr__(self):
        return f'Item {self.name}'