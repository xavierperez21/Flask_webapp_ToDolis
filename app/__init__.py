from flask import Flask
from flask_bootstrap import Bootstrap

from .config import Config
from .auth import auth


def create_app():
    # Creating a new instance of Flask
    app = Flask(__name__)   # __name__ is the name of this file "main.py"
    # Initializing flask-bootstrap extension
    bootstrap = Bootstrap(app)

    # Configuration of the app
    app.config.from_object(Config)

    # Registering the Blueprints
    app.register_blueprint(auth)
    
    return app
