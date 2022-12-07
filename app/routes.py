"""
RE STRUCTURING OUR APPLICATION : CONTROLLER (ROUTING AND RETURNING)

"""
# Referenced from the APP/__init__.py  and import the variable "APP"
from app import app
# Import render_template from flask
from flask import render_template
# Referenced from the directory APP/Models/Models.py then import the class Items.
from app.models.models import Items
# Referenced from the directory APP/Models/Forms.py then import the class RegisterForm.
from app.models.forms import RegisterForm



# Flask Routing
@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():

    # Reference the items to the Items(Model) and query it to the database.
    items = Items.query.all()

    # The arguments after the html referes to the variables above and pass it to the market html
    return render_template('market.html',items = items)


@app.route('/register')
def register_page():
    # Initialize the form
    form = RegisterForm()
    
    # Check if the user have submitted 
    # if form.validate_on_submit():


    # The arguments after the html referes to the variables above and pass it to register html
    return render_template('register.html',form = form)

@app.route('/login')
def method_name():
    pass