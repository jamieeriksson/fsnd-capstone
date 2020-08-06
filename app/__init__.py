from app.database.models import db_drop_and_create_all
from flask import Flask
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, populate_db
import os


def create_app(testing):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.DevConfig")

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_TEST_URI")

    CORS(app)
    setup_db(app)

    with app.app_context():
        from . import routes  # Import routes

        db_drop_and_create_all()
        populate_db()

        return app
