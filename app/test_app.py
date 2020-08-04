import unittest
import json
import os
from . import routes
from .database.models import Player, Team
from app import create_app, db
from flask_sqlalchemy import SQLAlchemy


class UltimatePlayersAndTeamsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.database_path = os.getenv("DATABASE_TEST_URI")
        self.client = self.app.test_client

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
        response = self.client().post("/players", json=self.new_player)
        response2 = self.client().post("/players", json=self.new_player_no_team)
        data = json.loads(response.data)
        data2 = json.loads(response2.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data2["success"], True)
        self.assertTrue(data["player"])
        self.assertTrue(data2["player"])

    def test_422_if_create_player_malformed_data(self):
        response = self.client().post("/players", json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_get_players(self):
        response = self.client().get("/players")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["players"])
        self.assertTrue(len(data["total_players"]))

    def test_404_if_page_contains_no_players(self):
        response = self.client().get("/players?page=1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_player_details_by_id(self):
        player = Player.query.filter_by(name="Billy Bob").first()
        response = self.client().get(f"/players/{player.id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["player"])
        self.assertEqual(data["player"], player.format())

    def test_404_if_player_not_found_by_id(self):
        response = self.client().get("/players/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_update_player(self):
        player = Player.query.filter_by(name="Billy Bob").first()
        response = self.client().patch(f"/players/{player.id}", json=self.update_player)
        data = json.loads(response.data)

        new_info = {
            "id": player.id,
            "name": "Billy Bob",
            "gender": "M",
            "jersey_number": 32,
            "position": "Cutter",
            "team_id": 1,
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["new_player_info"], new_info)
        self.assertTrue(data["previous_player_info"])

    def test_422_if_update_player_malformed_data(self):
        response = self.client().post("/players", json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_404_if_update_player_not_found_by_id(self):
        response = self.client().patch("/players/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_player_by_id(self):
        player = Player.query.filter_by(name="Billy Bob").first()
        response = self.client().delete(f"/players/{player.id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], player.id)

    def test_404_if_delete_player_id_not_found(self):
        response = self.client().delete("/players/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
