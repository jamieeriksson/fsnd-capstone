from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from flask import request, abort, jsonify
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.DevConfig")

    CORS(app)

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes

        # db.drop_all()
        # db.create_all()  # Create sql tables for our data models

        return app

