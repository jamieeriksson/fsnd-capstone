from flask import request, jsonify, abort
from datetime import datetime as dt
from flask import current_app as app
from .database.models import db, Player, Team
from .auth.auth import AuthError, requires_auth

ENTRIES_PER_PAGE = 20


@app.route("/")
def index():
    return jsonify(
        {
            "message": "Visit the /players or /teams routes to see player and team details!"
        }
    )


@app.route("/players", methods=["GET"])
def players():
    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        player_query = Player.query.paginate(page=page, per_page=ENTRIES_PER_PAGE)
        players_total = player_query.total

        if players_total == 0 or player_query == 0:
            abort(404)

        players = [player.format() for player in player_query.items]

        return jsonify(
            {"success": True, "total_players": players_total, "players": players}
        )
    else:
        abort(405)


@app.route("/players", methods=["POST"])
@requires_auth("create:players")
def new_player(jwt):
    if request.method == "POST":
        try:
            body = request.get_json()
            name = body.get("name")
            gender = body.get("gender")
            jersey_number = body.get("jersey_number")
            position = body.get("position")
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
            abort(422)
    else:
        abort(405)


@app.route("/players/<int:player_id>", methods=["GET"])
def player_details(player_id):
    if request.method == "GET":
        player = Player.query.filter_by(id=player_id).one_or_none()

        if player is None:
            abort(404)

        return jsonify({"success": True, "player": player.format()})
    else:
        abort(405)


@app.route("/players/<int:player_id>", methods=["PATCH"])
@requires_auth("update:players")
def update_player_details(jwt, player_id):
    if request.method == "PATCH":
        player = Player.query.filter_by(id=player_id).one_or_none()
        if player is None:
            abort(404)
        previous_player_info = player.format()
        body = request.get_json()
        player.name = body.get("name")
        player.gender = body.get("gender")
        player.jersey_number = body.get("jersey_number")
        player.position = body.get("position")
        team_id = body.get("team_id", None)
        try:
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
            abort(422)
    else:
        abort(405)


@app.route("/players/<int:player_id>", methods=["DELETE"])
@requires_auth("delete:players")
def delete_player(jwt, player_id):
    if request.method == "DELETE":
        player = Player.query.filter_by(id=player_id).one_or_none()
        if player is None:
            abort(404)
        try:

            player.delete()

            return jsonify({"success": True, "deleted": player_id})
        except:
            db.session.rollback()
            abort(422)
    else:
        abort(405)


@app.route("/teams", methods=["GET"])
def teams():
    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        team_query = Team.query.paginate(page=page, per_page=ENTRIES_PER_PAGE)
        teams_total = team_query.total

        if teams_total == 0:
            abort(404)

        teams = [team.format() for team in team_query.items]

        return jsonify({"success": True, "total_teams": teams_total, "teams": teams})

    else:
        abort(405)


@app.route("/teams", methods=["POST"])
@requires_auth("create:teams")
def new_team(jwt):
    if request.method == "POST":
        try:
            body = request.get_json()
            name = body.get("name")
            location = body.get("location")
            division = body.get("division")
            level = body.get("level")

            new_team = Team(
                name=name, location=location, division=division, level=level,
            )

            new_team.insert()

            return jsonify({"success": True, "team": new_team.format()})
        except:
            db.session.rollback()
            abort(422)
    else:
        abort(405)


@app.route("/teams/<int:team_id>", methods=["GET"])
def team_details(team_id):
    if request.method == "GET":
        team = Team.query.filter_by(id=team_id).one_or_none()

        if team is None:
            abort(404)

        return jsonify({"success": True, "team": team.format()})
    else:
        abort(405)


@app.route("/teams/<int:team_id>", methods=["PATCH"])
@requires_auth("update:teams")
def update_team_details(jwt, team_id):
    if request.method == "PATCH":
        team = Team.query.filter_by(id=team_id).one_or_none()
        if team is None:
            abort(404)
        previous_team_info = team.format()
        body = request.get_json()
        team.name = body.get("name")
        team.location = body.get("location")
        team.division = body.get("division")
        team.level = body.get("level")
        try:

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
            abort(422)
    else:
        abort(405)


@app.route("/teams/<int:team_id>", methods=["DELETE"])
@requires_auth("delete:teams")
def delete_team(jwt, team_id):
    if request.method == "DELETE":
        team = Team.query.filter_by(id=team_id).one_or_none()
        if team is None:
            abort(404)
        try:

            team.delete()

            return jsonify({"success": True, "deleted": team_id})
        except:
            db.session.rollback()
            abort(422)
    else:
        abort(405)


@app.errorhandler(404)
def page_not_found(e):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )


@app.errorhandler(405)
def page_not_found(e):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed"}),
        405,
    )


@app.errorhandler(422)
def unprocessable(error):
    return (jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422)


@app.errorhandler(AuthError)
def not_found(AuthError):
    return (
        jsonify(
            {
                "success": False,
                "error": AuthError.status_code,
                "message": AuthError.error,
            }
        ),
        AuthError.status_code,
    )
