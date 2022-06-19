"""The application initialization."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from website.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "index"


def create_app(config_class=Config):
    """Creates and configures Flask application.

    Returns:
        app: The configured and created application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from website.admin.routes import admin
    from website.user.routes import user
    from website.auth.routes import auth
    from website.task.routes import task
    from website.labeling.routes import labeling
    from website.main.routes import main
    from website.export_convert.routes import export_convert

    from website.errors.handlers import errors

    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(task)
    app.register_blueprint(labeling)
    app.register_blueprint(main)
    app.register_blueprint(export_convert)
    app.register_blueprint(errors)

    return app
