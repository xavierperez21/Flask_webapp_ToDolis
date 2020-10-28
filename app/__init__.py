from flask import Flask
from flask_bootstrap import Bootstrap

from .config import Config


def create_app():
    # Creating a new instance of Flask
    app = Flask(__name__)   # __name__ is the name of this file "main.py"
    # Initializing flask-bootstrap extension
    bootstrap = Bootstrap(app)

    # Assigning the secret key to create a user session.
    app.config.from_object(Config)
    
    return app
