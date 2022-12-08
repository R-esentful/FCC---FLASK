"""
RE STRUCTURING OUR APPLICATION : CONTROLLER (ROUTING AND RETURNING)

"""
# Referenced from the APP/__init__.py  and import the variable "APP","DB".
from app import app,db
# Import render_template,redirect(for redirecting the webpage),flash (for displaying error in form validation),get_flashed_messages( GETS THE FLASHED MESSAGE. PLEASE REFER TO BASE HTML ) from flask
from flask import render_template,redirect,url_for,flash,get_flashed_messages
# Referenced from the directory APP/Models/Models.py then import the class Items,User.
from app.models.models import Items,User
# Referenced from the directory APP/Models/Forms.py then import the class RegisterForm,LoginForm.
from app.models.forms import RegisterForm,LoginForm



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


@app.route('/register',methods = ['GET','POST'])
def register_page():
    # Initialize the form
    form = RegisterForm()
    
    # Check if the user have submitted 
    # Validations
    if form.validate_on_submit():

        # Create Instance for the user
        # instead of passing the password_hash from the model, we then pass the @property we have created
        user_to_create = User(username=form.username.data,email_address = form.email_address.data , password = form.password1.data)
        
        # Database session for comitting
        db.session.add(user_to_create)
        db.session.commit()

        # Redirects the user to the market page
        return redirect(url_for('market_page'))
    
    # If there are errors received from the form validation
    if form.errors != {}:
        # Iterates through the error message
        for err_msg in form.errors.values():
            # Flashes the message, it has the categories indicated within the base html which is the with_categories.
            flash(f'There was an error with creating a user {err_msg}',category = 'danger')
    
    # The arguments after the html referes to the variables above and pass it to register html
    return render_template('register.html',form = form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()

    #form.validate_on_submit():


    return render_template('login.html',form = form)