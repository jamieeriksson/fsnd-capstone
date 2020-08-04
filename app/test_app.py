import unittest
import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# from app import routes

# from app import create_app, db
from .database.models import Player, Team
from flask_sqlalchemy import SQLAlchemy

# from app.auth.auth import AuthError
db = SQLAlchemy()


class UltimatePlayersAndTeamsTestCase(unittest.TestCase):
    def setUp(self):
        def create_app(self):
            app = Flask(__name__)
            app.config["TESTING"] = True
            app.config["WTF_CSRF_ENABLED"] = False
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
            app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_TEST_URI")
            db.init_app(app)

            with app.app_context():
                db.create_all()  # Create sql tables for our data models

                return app

        self.app = create_app(self)

        self.admin_jwt = os.getenv("ADMIN_TOKEN")
        self.team_manager_jwt = os.getenv("TEAM_MANAGER_TOKEN")
        self.client = self.app.test_client

        self.admin_headers = {"Authorization": f'Bearer {os.getenv("ADMIN_TOKEN")}'}
        self.team_manager_headers = {
            "Authorization": f'Bearer {os.getenv("TEAM_MANAGER_TOKEN")}'
        }

        self.new_player = {
            "name": "Billy Bob",
            "gender": "M",
            "jersey_number": 4,
            "position": "Handler",
            "team_id": 1,
        }

        self.update_player = {
            "name": "Billy Bob",
            "gender": "M",
            "jersey_number": 32,
            "position": "Cutter",
            "team_id": 1,
        }

        self.new_player_no_team = {
            "name": "Billy Bob",
            "gender": "M",
            "jersey_number": 4,
            "position": "Handler",
        }

        self.new_team = {
            "name": "WOOF",
            "location": "Richardson, TX",
            "division": "Open",
            "level": "College",
        }

    def tearDown(self):
        pass

    def test_create_new_player(self):
        response = self.client().post(
            "/players", json=self.new_player, headers=self.admin_headers
        )
        response2 = self.client().post(
            "/players", json=self.new_player_no_team, headers=self.admin_headers
        )
        print(response)
        data = json.loads(response.data)
        data2 = json.loads(response2.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data2["success"], True)
        self.assertTrue(data["player"])
        self.assertTrue(data2["player"])

    # def test_422_if_create_player_malformed_data(self):
    #     response = self.client().post("/players", json={}, headers=self.admin_headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")

    # def test_401_team_manager_cannot_post_player(self):
    #     response = self.client().post(
    #         "/players", json=self.new_player, headers=self.team_manager_headers
    #     )
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "User does not have permission")

    # def test_401_regular_user_cannot_post_player(self):
    #     response = self.client().post("/players", json=self.new_player)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Header Not Present")

    def test_get_players(self):
        response = self.client().get("/players")
        print(response)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["players"])
        self.assertTrue(len(data["total_players"]))

    # def test_404_if_page_contains_no_players(self):
    #     response = self.client().get("/players?page=1000")
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_get_player_details_by_id(self):
    #     player = Player.query.filter_by(name="Billy Bob").first()
    #     response = self.client().get(f"/players/{player.id}")
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["player"])
    #     self.assertEqual(data["player"], player.format())

    # def test_404_if_player_not_found_by_id(self):
    #     response = self.client().get("/players/1000")
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_update_player(self):
    #     player = Player.query.filter_by(name="Billy Bob").first()
    #     response = self.client().patch(
    #         f"/players/{player.id}", json=self.update_player, headers=self.admin_headers
    #     )
    #     data = json.loads(response.data)

    #     new_info = {
    #         "id": player.id,
    #         "name": "Billy Bob",
    #         "gender": "M",
    #         "jersey_number": 32,
    #         "position": "Cutter",
    #         "team_id": 1,
    #     }

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["new_player_info"], new_info)
    #     self.assertTrue(data["previous_player_info"])

    # def test_422_if_update_player_malformed_data(self):
    #     player = Player.query.filter_by(name="Billy Bob").first()
    #     response = self.client().patch(
    #         f"/players/{player.id}", json={}, headers=self.admin_headers
    #     )
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")

    # def test_404_if_update_player_not_found_by_id(self):
    #     response = self.client().patch(
    #         "/players/1000", json=self.update_player, headers=self.admin_headers
    #     )
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_401_team_manager_cannot_update_player(self):
    #     player = Player.query.filter_by(name="Billy Bob").first()
    #     response = self.client().patch(
    #         f"/players/{player.id}",
    #         json=self.update_player,
    #         headers=self.team_manager_headers,
    #     )
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "User does not have permission")

    # def test_401_regular_user_cannot_update_player(self):
    #     player = Player.query.filter_by(name="Billy Bob").first()
    #     response = self.client().patch(f"/players/{player.id}", json=self.update_player)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Header Not Present")

    # def test_delete_player_by_id(self):
    #     player = Player.query.filter_by(name="Billy Bob").first()
    #     response = self.client().delete(
    #         f"/players/{player.id}", headers=self.admin_headers
    #     )
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], player.id)

    # def test_404_if_delete_player_id_not_found(self):
    #     response = self.client().delete("/players/1000", headers=self.admin_headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_401_team_manager_cannot_update_player(self):
    #     player = Player.query.filter_by(name="Billy Bob").first()
    #     response = self.client().delete(
    #         f"/players/{player.id}", headers=self.team_manager_headers
    #     )
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "User does not have permission")

    # def test_401_regular_user_cannot_update_player(self):
    #     player = Player.query.filter_by(name="Billy Bob").first()
    #     response = self.client().delete(f"/players/{player.id}")
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Headers Not Present")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
