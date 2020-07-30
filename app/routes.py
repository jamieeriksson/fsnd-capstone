from operator import pos
from flask import request, jsonify, abort
from datetime import datetime as dt
from flask import current_app as app
from .database.models import db, Player, Team

ENTRIES_PER_PAGE = 20


@app.route("/players", methods=["GET", "POST"])
def players():
    if request.method == "GET":
        try:
            page = request.args.get("page", 1)
            player_query = Player.query.paginate(page=page, per_page=ENTRIES_PER_PAGE)
            players_total = player_query.total
            players = [player.format() for player in player_query.items]

            return jsonify(
                {"success": True, "total_players": players_total, "players": players}
            )
        except:
            db.session.rollback()
            abort(400)
    else:
        try:
            body = request.get_json()
            name = body.get("name", "")
            gender = body.get("gender", "")
            jersey_number = body.get("jersey", 1)
            position = body.get("position", "")
            team_id = body.get("team_id", None)
            team = Team.query.filter_by(id=team_id).one_or_none() if team_id else None

            new_player = Player(
                name=name,
                gender=gender,
                jersey_number=jersey_number,
                position=position,
            )
            new_player.team = team

            db.session.add(new_player)
            db.session.commit()

            return jsonify({"success": True, "player": new_player.format()})
        except:
            db.session.rollback()
            abort(400)


@app.route("/teams", methods=["GET", "POST"])
def teams():
    if request.method == "GET":
        page = request.args.get("page", 1)
        team_query = Team.query.paginate(page=page, per_page=ENTRIES_PER_PAGE)
        teams_total = team_query.total
        teams = [team.format() for team in team_query.items]

        return jsonify({"teams": teams_total, "teams": teams})

