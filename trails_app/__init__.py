# App metadata
__version__ = "0.2.0"

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from pathlib import Path
import os
from omegaconf import DictConfig, open_dict

# Database imports
from . import models
from .models import db
from .models import User

# Blueprint imports
from .auth import auth as auth_blueprint
from .main import main as main_blueprint

# APP FACTORY FUNCTION --------------------------------------------------------


def create_app(config: DictConfig):
    """Flask app factory function"""

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    # Ensure the instance folder exists
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # Initialize database
    db.init_app(app)

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
