from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
from .database.models import db, Player, Team

ENTRIES_PER_PAGE = 20


@app.route("/players", methods=["GET", "POST"])
def players():
    if request.method == "GET":
        page = request.args.get("page", 1)
        player_query = Player.query.paginate(page=page, per_page=ENTRIES_PER_PAGE)
        players_total = player_query.total
        players = [player.format() for player in player_query.items]

        return jsonify({"total_players": players_total, "players": players})


@app.route("/teams", methods=["GET", "POST"])
def teams():
    if request.method == "GET":
        page = request.args.get("page", 1)
        team_query = Team.query.paginate(page=page, per_page=ENTRIES_PER_PAGE)
        teams_total = team_query.total
        teams = [team.format() for team in team_query.items]

        return jsonify({"teams": teams_total, "teams": teams})

