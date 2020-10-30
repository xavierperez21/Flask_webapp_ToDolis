from flask import render_template, session, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from app.forms import LoginForm
from app.firestore_service import get_user
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

            # Validating password
            if password == password_from_db:
                # Making login of the user through the creation of a new instance of UserData and UserModel
                # That will be send to a function 'login_user()' from flask-login
                user_data = UserData(username, password)
                user = UserModel(user_data)
                
                # Login our User in flask_login, so flask_login knows that there's a current user
                login_user(user)
                
                flash('Bienvenido de nuevo!')

                redirect(url_for('hello'))
            
            else:
                flash('La información no coincide :(')

        else:
            flash('El usuario no existe')

        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    return render_template('signup.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()   # flask_login makes logout of the current user
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))