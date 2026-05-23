import os
import unittest

os.environ["FLASK_ENV"] = "testing"

from app import create_app
from app.models import db


class SensusSmokeTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()

    def test_web_and_health_are_available(self):
        home = self.client.get("/")
        health = self.client.get("/api/health")

        self.assertEqual(home.status_code, 200)
        self.assertIn(b"Sensus", home.data)
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.get_json()["status"], "ok")

    def test_demo_user_can_login_and_list_accounts(self):
        demo = self.client.post("/api/demo/seed", json={})
        self.assertEqual(demo.status_code, 201)

        login = self.client.post(
            "/api/auth/login",
            json={"email": "demo@sensus.local", "password": "demo123"},
        )
        self.assertEqual(login.status_code, 200)

        user_id = login.get_json()["user"]["id"]
        accounts = self.client.get(f"/api/accounts?user_id={user_id}")
        self.assertEqual(accounts.status_code, 200)
        self.assertGreaterEqual(len(accounts.get_json()["accounts"]), 1)


if __name__ == "__main__":
    unittest.main()
