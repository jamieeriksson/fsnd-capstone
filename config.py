from os import environ, path
import os
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    ENV = "production"
    DEBUG = False
    TESTING = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    TESTING = True
