import unittest
from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user

from app import create_app
from app.forms import ToDoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_service import get_todos, put_todo, delete_todo, update_todo

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


#----------- Routes --------------------

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


# Decorator to indicate the route where this function will be executed.
@app.route('/hello', methods=['GET', 'POST'])
@login_required     # This decorator must be after the route decorator. If there's no a current_user, this route is blocked
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id  # Once the form is validated, we get the username after the redirection
    todo_form = ToDoForm()      # To create to-dos
    delete_form = DeleteTodoForm()  # To delete to-dos
    update_form = UpdateTodoForm()
    
    # Creating a new variable "context" which is a dictionary that will contain all the variables we want to pass to the template
    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form,
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)

        flash('Todo succesfully registered')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context) # Expanding the dictionary using **context.


# This is a dynamic route
@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))


# This is a dynamic route
@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id

    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    print(done)
    
    return redirect(url_for('hello'))