"""Configuration specification for development and testing environment."""

import os


class Config:
    """Configures the application for development purposes."""

    SECRET_KEY = 'secret-key-to-be-changed' # os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    HEAD = 0
    LABELS = []
    CURRENTLY_IN_PROGRESS = []


class TestingConfig:
    """Configures the application for testing purposes."""

    DB_SERVER = "localhost"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_site.db"
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    TESTING = True
    LOGIN_DISABLED = True
    HEAD = 0
    LABELS = []
    CURRENTLY_IN_PROGRESS = []