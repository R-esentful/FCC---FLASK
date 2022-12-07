"""
FLASK FORM HANDLING. FLASK HAS A BUILT IN FORM HANDLING WHICH IS FLASK WTF
"""
# Import FlaskForm which is Similar to the db.Model
from flask_wtf import FlaskForm
# From wtforms import the fields. These fields are responsible for handling inputs such as Password, Email and etc.
from wtforms import StringField,PasswordField,SubmitField


"""
In flask forms, a class must inherit the imported FlaskForm from flask_wtf module

StringField = A field for strings
PasswordField = A field for passwords
SubmitField = A field/button for submission

Parameters:
    label = Similar with HTML Labels. It sets the label for the Input (Optional if u want to customize your own label field)

"""

# Register Form
class RegisterForm(FlaskForm):
    username = StringField(label = 'username')
    email_address = StringField(label = 'Email')
    password1 = PasswordField(label = 'Password1')
    password2 = PasswordField(label = 'Password2')
    submit = SubmitField(label = 'Create Account')