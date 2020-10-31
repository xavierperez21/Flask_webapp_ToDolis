import firebase_admin
from firebase_admin import credentials  # This library will let us authenticate in the console when we want to communicate with firestore
from firebase_admin import firestore

credential = credentials.ApplicationDefault()   # this is because we made a "gcloud auth application-default login"
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()


def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)    # Creating automatically a new user document
    user_ref.set({ 'password': user_data.password })    # Finishing on register the new user by assing the parameter password with the hashed password


def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()


def put_todo(user_id, description):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    
    # Adding a description property in the new todo document
    todos_collection_ref.add({ 'description': description, 'done': False })


def delete_todo(user_id, todo_id):
    # Another way to obtain the reference of a todo:
    # todo_ref = db.document('users/{}/todos/{}'.format(user_id, todo_id))
    
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()


def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)  # When we submit the form update, we switch the value it had before.
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({ 'done': todo_done })


def _get_todo_ref(user_id, todo_id):
    return db.collection('users').document(user_id).collection('todos').document(todo_id)