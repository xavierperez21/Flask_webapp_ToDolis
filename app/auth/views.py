from flask import render_template, session, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from app.forms import LoginForm
from app.firestore_service import get_user, user_put
from app.models import UserModel, UserData

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('hello'))

    login_form = LoginForm()

    context = {
        'login_form': login_form
    }

    # If the form was filled correctly
    if login_form.validate_on_submit():
        username = login_form.username.data     # Getting the username from the form
        password = login_form.password.data    # Getting the password from the form

        user_doc = get_user(username)   # Getting the user doc from the db

        # Validating if the username exists
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']   # Obtaining the password from the db

            # Validating hashed password
            if check_password_hash(password_from_db, password):
                # Making login of the user through the creation of a new instance of UserData and UserModel
                # That will be send to a function 'login_user()' from flask-login
                user_data = UserData(username, password)
                user = UserModel(user_data)
                
                # Login our User in flask_login, so flask_login knows that there's a current user
                # From here, we send an instance of UserModel that flask_login to later use the method...
                # ... 'get_id' which will send the id of the user to the login_manager.user_loader so ...
                # ... flask_login creates a current user and the route /hello gets unblocked.
                login_user(user)
                
                flash('Welcome again!')

                redirect(url_for('hello'))
            
            else:
                flash("The information doesn't match :(")

        else:
            flash("The user doesn't exists")

        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        # Validating if the user doesn't exist
        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)    # Hashing the password
            user_data = UserData(username, password_hash)       # Generating a UserData instance that will be added to the db
            
            user_put(user_data)     # We register the user with the object UserData and not with the UserModel because the db doesn't need a UserModel as flask_login
            
            # Login after we register the user
            user = UserModel(user_data)
            login_user(user)
            flash('Welcome!')

            return redirect(url_for('hello'))

        else:
            flash('The user already exists!')

    return render_template('signup.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()   # flask_login makes logout of the current user
    flash('Come back soon!')

    return redirect(url_for('auth.login'))