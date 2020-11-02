from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .config import Config
from .auth import auth
from .models import UserModel


login_manager = LoginManager()

# The route that login_manager manages (So, this will be the first route that...
# ...will appear to protect the route we want) the protected route will have a...
# ... decorator like @login_required
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    print(username)
    return UserModel.query(username)


def create_app():
    # Creating a new instance of Flask
    app = Flask(__name__)   # __name__ is the name of this file "main.py"

    # Initializing flask-bootstrap extension
    bootstrap = Bootstrap(app)

    # Configuration of the app
    app.config.from_object(Config)

    # Initialize the app with login_manager so this login_manager knows the structurre of the app.
    login_manager.init_app(app)

    # Registering the Blueprints
    app.register_blueprint(auth)
    
    return app
