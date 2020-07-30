from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .database.models import db, Player, Team


@app.route("/", methods=["GET"])
def say_hello():
    return "My app and routes are working!"

