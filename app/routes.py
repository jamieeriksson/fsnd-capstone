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


@app.route("/players/<int:player_id>", methods=["GET", "PATCH", "DELETE"])
def player_details(player_id):
    if request.method == "PATCH":
        try:
            player = Player.query.filter_by(id=player_id).one_or_none()
            previous_player_info = player.format()
            if player is None:
                abort(400)

            body = request.get_json()
            player.name = body.get("name", "")
            player.gender = body.get("gender", "")
            player.jersey_number = body.get("jersey", 1)
            player.position = body.get("position", "")
            team_id = body.get("team_id", None)
            player.team = (
                Team.query.filter_by(id=team_id).one_or_none() if team_id else None
            )

            db.session.commit()

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

            db.session.delete(player)
            db.session.commit()

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

            db.session.add(new_team)
            db.session.commit()

            return jsonify({"success": True, "team": new_team.format()})
        except:
            db.session.rollback()
            abort(400)

