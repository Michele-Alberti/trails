# App metadata
__version__ = "0.0.1"

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from pathlib import Path
import os

# Database imports
from . import models
from .models import db
from .models import User

# Blueprint imports
from .auth import auth as auth_blueprint
from .main import main as main_blueprint

# APP FACTORY FUNCTION --------------------------------------------------------


def create_app(test_config=None):
    """Flask app factory function"""

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
        SQLALCHEMY_DATABASE_URI="sqlite:///trails.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # Initialize database
    db.init_app(app)

    # Register cli commands
    app.cli.add_command(models.init_db_command)

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # user_id is the primary key of users table
        return User.query.get(int(user_id))

    # CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Auth blueprint registration
    app.register_blueprint(auth_blueprint)

    # Non-auth blueprnt registration
    app.register_blueprint(main_blueprint)

    return app
