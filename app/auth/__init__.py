from flask import Blueprint

# Blueprint( name of the blueprint, 
#            name of the file .py, 
#            url_prefix means that every route that starts with '/auth' will be redirected to this blueprint )
auth = Blueprint('auth', __name__, url_prefix='/auth')

# We have to import all the views after we create the blueprint to configurate the application
from . import views