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

            new_player.insert()

            return jsonify({"success": True, "player": new_player.format()})
        except:
            db.session.rollback()
            abort(400)


@app.route("/players/<int:player_id>", methods=["GET", "PATCH", "DELETE"])
def player_details(player_id):
    if request.method == "PATCH":
        try:
            player = Player.query.filter_by(id=player_id).one_or_none()
            if player is None:
                abort(400)
            previous_player_info = player.format()

            body = request.get_json()
            player.name = body.get("name", "")
            player.gender = body.get("gender", "")
            player.jersey_number = body.get("jersey", 1)
            player.position = body.get("position", "")
            team_id = body.get("team_id", None)
            player.team = (
                Team.query.filter_by(id=team_id).one_or_none() if team_id else None
            )

            player.update()

            return jsonify(
                {
                    "success": True,
                    "new_player_info": player.format(),
                    "previous_player_info": previous_player_info,
                }
            )
        except:
            db.session.rollback()
            abort(400)
    elif request.method == "DELETE":
        try:
            player = Player.query.filter_by(id=player_id).one_or_none()
            if player is None:
                abort(400)

            player.delete()

            return jsonify({"success": True, "deleted": player_id})
        except:
            db.session.rollback()
            abort(400)
    elif request.method == "GET":
        player = Player.query.filter_by(id=player_id).one_or_none()
        if player is None:
            abort(400)
        return jsonify({"success": True, "player": player.format()})
    else:
        abort(400)


@app.route("/teams", methods=["GET", "POST"])
def teams():
    if request.method == "GET":
        try:
            page = request.args.get("page", 1)
            team_query = Team.query.paginate(page=page, per_page=ENTRIES_PER_PAGE)
            teams_total = team_query.total
            teams = [team.format() for team in team_query.items]

            return jsonify({"teams": teams_total, "teams": teams})
        except:
            db.session.rollback()
            abort(400)
    else:
        try:
            body = request.get_json()
            name = body.get("name", "")
            location = body.get("location", "")
            division = body.get("division", "")
            level = body.get("level", "")

            new_team = Team(
                name=name, location=location, division=division, level=level,
            )

            new_team.insert()

            return jsonify({"success": True, "team": new_team.format()})
        except:
            db.session.rollback()
            abort(400)


@app.route("/teams/<int:team_id>", methods=["GET", "PATCH", "DELETE"])
def team_details(team_id):
    if request.method == "PATCH":
        try:
            team = Team.query.filter_by(id=team_id).one_or_none()
            if team is None:
                abort(400)
            previous_team_info = team.format()

            body = request.get_json()
            team.name = body.get("name", "")
            team.location = body.get("location", "")
            team.division = body.get("division", "")
            team.level = body.get("level", "")

            team.update()

            return jsonify(
                {
                    "success": True,
                    "new_team_info": team.format(),
                    "previous_team_info": previous_team_info,
                }
            )
        except:
            db.session.rollback()
            abort(400)
    elif request.method == "DELETE":
        try:
            team = Team.query.filter_by(id=team_id).one_or_none()
            if team is None:
                abort(400)

            team.delete()

            return jsonify({"success": True, "deleted": team_id})
        except:
            db.session.rollback()
            abort(400)
    elif request.method == "GET":
        team = Team.query.filter_by(id=team_id).one_or_none()
        if team is None:
            abort(400)
        return jsonify({"success": True, "team": team.format()})
    else:
        abort(400)
