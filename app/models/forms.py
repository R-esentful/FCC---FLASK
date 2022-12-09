"""
FLASK FORM HANDLING. FLASK HAS A BUILT IN FORM HANDLING WHICH IS FLASK WTF
"""
# Import FlaskForm which is Similar to the db.Model
from flask_wtf import FlaskForm
# From wtforms import the fields. These fields are responsible for handling inputs such as Password, Email and etc.
from wtforms import StringField,PasswordField,SubmitField
# Module for setting validators for our forms. e.g the username's length should be maximum of 12
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError

# Referenced from the directory APP/Models/Models.py then import the class Items,User.
from app.models.models import User
"""
In flask forms, a class must inherit the imported FlaskForm from flask_wtf module

StringField = A field for strings
PasswordField = A field for passwords
SubmitField = A field/button for submission

Parameters:
    label = Similar with HTML Labels. It sets the label for the Input 
            (Optional if u want to customize your own label field)
    validators = Sets validators from wtforms

Note the validator parameters can be multiple type of validators. E.g [Length(),EqualTo()]

Validators parameters:
    Length = Sets the length of the form field. Min length and max 
             length are its sub parameters. 
    EqualTo = validates if the form field has the same value
    Email = checks if the form input field is email. 
    (Make sure to install email_validator in our environment)
    DataRequired = Verify if fields has Data or has information

    ValidationError = raises validation error from forms and transfers it to the route for error message

"""

# Register Form
class RegisterForm(FlaskForm):

    # function for validating username in SQLAlchemy.
    # It checks if the username already exists in the database.
    # parameter username_to_check is used to pass the username
    # validate_ - validates the form field
    # validate_username - validates the username field 
    def validate_username(self,username_to_check):
        # create a query for checking the user
        # it is important to have .first() since this grabs the object.
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            # raises validation error to be transfered to the route form error.
            raise ValidationError('Username already exists please try again')

    def validate_email_address(self,email_address_to_check):
        # creates a query for checking the email_address
        # it is important to have .first() since this grabs the object.
        email = User.query.filter_by(email_address = email_address_to_check.data).first()

        if email:
            # raises validation error to be transfered to the route form error.
            raise ValidationError('Email Aldready exists please try again!')


    username = StringField(label = 'username',validators = [Length(min =2,max = 30),DataRequired()])
    
    email_address = StringField(label = 'Email',validators = [Email(),DataRequired()])
    password1 = PasswordField(label = 'Password1',validators = [Length(min =6),DataRequired()])
    password2 = PasswordField(label = 'Password2',validators = [EqualTo('password1'),DataRequired()])
    submit = SubmitField(label = 'Create Account')

# Login Form
class LoginForm(FlaskForm):
    username = StringField(label = 'Username',validators = [DataRequired()])
    password = PasswordField(label = 'Password',validators = [DataRequired()])
    submit = SubmitField(label = 'Submit')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label = 'Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label = 'Sell Item')