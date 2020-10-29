import firebase_admin
from firebase_admin import credentials  # This library will let us authenticate in the console when we want to communicate with firestore
from firebase_admin import firestore

credential = credentials.ApplicationDefault()   # this is because we made a "gcloud auth application-default login"
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()