"""
RE STRUCTURING OUR APPLICATION : CONTROLLER (ROUTING AND RETURNING)

"""
# Referenced from the APP/__init__.py  and import the variable "APP","DB".
from app import app,db
# Import render_template,redirect(for redirecting the webpage),flash (for displaying error in form validation),get_flashed_messages( GETS THE FLASHED MESSAGE. PLEASE REFER TO BASE HTML ),request(checks the method being sent) from flask
from flask import render_template,redirect,url_for,flash,get_flashed_messages,request
# Referenced from the directory APP/Models/Models.py then import the class Items,User.
from app.models.models import Items,User
# Referenced from the directory APP/Models/Forms.py then import the class RegisterForm(For Registering),LoginForm(For Logging in),PurchaseItemForm(For Purchasing),SellItemForm(For selling).
from app.models.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
# from module flask login, we import login_user(logs the session of the user),logout_user(logs out the session of the user),login_required ( requires login authentication ),current_user(returns the )
from flask_login import login_user,logout_user,login_required,current_user


# Flask Routing
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market',methods = ['GET','POST'])
# Decorator if we want the user to login to view this webpage
@login_required
def market_page():
    # Initialize purchaseform
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    

    # Checks if the method is POST request
    if request.method == 'POST':

        # purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_obj = Items.query.filter_by(name = purchased_item).first()

        # Checks if the object exists
        if p_item_obj:
            # Method to check if the current user can purchase
            if current_user.can_purchase(p_item_obj):
                '''
                NOTE THAT WE CAN SIMPLIFY THIS CODE BLOCK BY 
                # Assigns obj owner by getting the current_user's ID
                -p_item_obj.owner = current_user.id
                # Deducts the budget of the current user to the item's price
                - current_user.budget -= p_item_obj.price
                # commites the changes to the database
                db.session.commit()
                '''
                p_item_obj.assign_item(current_user)
                
               

                flash(f'You have purchased {p_item_obj.name} for {p_item_obj.price}',category = 'success')
            else:
                flash(f'Insufficient balance. Please top up!',category = 'danger')
           
           

        # Selling item logic    
        sold_item = request.form.get('sold_item')
        s_item_obj = Items.query.filter_by(name = sold_item).first()
        
        # Checks if the object exists
        if s_item_obj:
            # Checks if the user owns the item.
            if current_user.can_sell(s_item_obj):
                #
                s_item_obj.sell_item(current_user)
                flash(f'Item {s_item_obj.name} have been sold for {s_item_obj.price}',category = 'success')
            else:
                flash('An error occured',category = 'Danger')

         # Redirects the user to the market page
        return redirect(url_for('market_page'))
    # Checks if the method is GET
    if request.method =='GET':
        # Reference the items to the Items(Model) and query it to the database.
        items = Items.query.filter_by(owner = None)

        # Queries the item owned by the current user
        owned_items = Items.query.filter_by(owner = current_user.id)

        # The arguments after the html referes to the variables above and pass it to the market html
        return render_template('market.html',items = items,purchase_form =purchase_form,owned_items = owned_items,selling_form = selling_form)

    
    


@app.route('/register',methods = ['GET','POST'])
def register_page():
    # Initialize the register form
    form = RegisterForm()
    
    # Check if the user have submitted 
    # Validations
    if form.validate_on_submit():

        # Create Instance for the user
        # instead of passing the password_hash from the model, we then pass the @property we have created
        user_to_create = User(username=form.username.data,email_address = form.email_address.data , password = form.password1.data)
        
        # Database session for adding and comitting
        db.session.add(user_to_create)
        db.session.commit()
        # logins the user
        login_user(user_to_create)
        # flashes message
        flash(f'Account created successfully. Logging in as {user_to_create.username}',category = 'success')

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
    # Initialize the Login Form
    form = LoginForm()

    # Check if the user have submitted 
    # Validations
    if form.validate_on_submit():
        # Creates a query in the User model through the form data
        attempted_user = User.query.filter_by(username = form.username.data).first()
        
        # checks if user exists and they have the same password.
        if attempted_user and attempted_user.check_password(attempted_password = form.password.data):
            # logins the user
            login_user(attempted_user)
            # flashes message
            flash(f'Logged in as {attempted_user.username}',category = 'success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or password do not match',category = 'danger')

    return render_template('login.html',form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('Successfully Logged out',category = 'info')
    return redirect(url_for('home_page'))