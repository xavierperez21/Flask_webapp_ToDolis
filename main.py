from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest

from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users, get_todos

# Creating a new instance of Flask
app = create_app()

#---------- CLI Commands ----------------------
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


#------------ Error handlers ------------
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    # Raise a 500 server error: raise(Exception('500 error'))
    
    # First we have to know the IP of the user
    user_ip = request.remote_addr   # IP of the user. This time the IP will be ours (127.0.0.1) but if our app is in production the IP will be the one of the user in any part of the world

    # Generating the response
    response = make_response(redirect('/hello'))
    # response.set_cookie('user_ip', user_ip)     # Generating a cookie to save the ip of the user so we can access to it in the route /hello
    
    # Getting the user's ip through the user's session
    session['user_ip'] = user_ip

    return response


#----------- Routes --------------------
# Decorator to indicate the route where this function will be executed.
@app.route('/hello', methods=['GET'])
def hello():
    user_ip = session.get('user_ip')

    # Once the form is validated, we get the username after the redirection
    username = session.get('username')
    # print(username)

    # Creating a new variable "context" which is a dictionary that will contain all the variables we want to pass to the template
    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username
    }

    users = get_users()

    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    return render_template('hello.html', **context) # Expanding the dictionary using **context.