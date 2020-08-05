import unittest
import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app import create_app
from app.database.models import db, Player, Team


class UltimateTeamsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = create_app(True)

        self.admin_jwt = os.getenv("ADMIN_TOKEN")
        self.team_manager_jwt = os.getenv("TEAM_MANAGER_TOKEN")
        self.client = self.app.test_client

        self.admin_headers = {"Authorization": f'Bearer {os.getenv("ADMIN_TOKEN")}'}
        self.team_manager_headers = {
            "Authorization": f'Bearer {os.getenv("TEAM_MANAGER_TOKEN")}'
        }

        self.team_name = "Teamify"

        self.new_team = {
            "name": "Public Enemy",
            "location": "Dallas, TX",
            "division": "Mixed",
            "level": "Club",
        }

        self.update_team = {
            "name": "Public Enemy",
            "location": "DFW, TX",
            "division": "Mixed",
            "level": "Masters",
        }

    def setUp(self):
        def populate_db():
            db.drop_all()
            db.create_all()
            new_team = Team(
                name="Teamify", location="Texas", division="Womens", level="Club",
            )
            new_team.insert()
            new_player = Player(
                name="Doe Johnson",
                gender="F",
                jersey_number=15,
                position="Hybrid",
                team_id=1,
            )

            new_player.insert()

        populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.session.close()

    def test_get_teams(self):
        response = self.client().get("/teams")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["teams"])
        self.assertTrue(data["total_teams"])

    def test_404_if_page_contains_no_teams(self):
        response = self.client().get("/teams?page=1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_team_details_by_id(self):
        team = Team.query.filter_by(name=self.team_name).first()
        response = self.client().get(f"/teams/{team.id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["team"])

    def test_404_if_team_not_found_by_id(self):
        response = self.client().get("/teams/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_team(self):
        response = self.client().post(
            "/teams", json=self.new_team, headers=self.admin_headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["team"])

    def test_422_if_create_team_malformed_data(self):
        response = self.client().post(
            "/teams", json={"not_a_key": "bad data"}, headers=self.admin_headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_401_team_manager_cannot_post_team(self):
        response = self.client().post(
            "/teams", json=self.new_team, headers=self.team_manager_headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "User does not have permission")

    def test_401_regular_user_cannot_post_team(self):
        response = self.client().post("/teams", json=self.new_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Header Not Present")

    def test_update_team(self):
        team = Team.query.filter_by(name=self.team_name).first()
        response = self.client().patch(
            f"/teams/{team.id}", json=self.update_team, headers=self.admin_headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["new_team_info"])
        self.assertTrue(data["previous_team_info"])

    def test_422_if_update_team_malformed_data(self):
        team = Team.query.filter_by(name=self.team_name).first()
        response = self.client().patch(
            f"/teams/{team.id}",
            json={"not_a_key": "bad data"},
            headers=self.admin_headers,
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_404_if_update_team_not_found_by_id(self):
        response = self.client().patch(
            "/teams/1000", json=self.update_team, headers=self.admin_headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_401_team_manager_cannot_update_team(self):
        team = Team.query.filter_by(name=self.team_name).first()
        response = self.client().patch(
            f"/teams/{team.id}",
            json=self.update_team,
            headers=self.team_manager_headers,
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "User does not have permission")

    def test_401_regular_user_cannot_update_team(self):
        team = Team.query.filter_by(name=self.team_name).first()
        response = self.client().patch(f"/teams/{team.id}", json=self.update_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Header Not Present")

    def test_delete_team_by_id(self):
        response = self.client().delete("/teams/1", headers=self.admin_headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)

    def test_404_if_delete_team_id_not_found(self):
        response = self.client().delete("/teams/1000", headers=self.admin_headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_401_team_manager_cannot_update_team(self):
        team = Team.query.filter_by(name=self.team_name).first()
        response = self.client().delete(
            f"/teams/{team.id}", headers=self.team_manager_headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "User does not have permission")

    def test_401_regular_user_cannot_update_team(self):
        team = Team.query.filter_by(name=self.team_name).first()
        response = self.client().delete(f"/teams/{team.id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Header Not Present")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
