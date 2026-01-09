import unittest
from app import app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.valid_user = {
            "first_name": "Ali",
            "last_name": "Ahmed",
            "email": "ali@test.com"
        }

    def test_create_user_success(self):
        response = self.client.post(
            "/api/v1/users",
            json=self.valid_user
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_user_missing_email(self):
        data = {
            "first_name": "Ali",
            "last_name": "Ahmed"
        }
        response = self.client.post("/api/v1/users", json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
        response = self.client.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)


if __name__ == "__main__":
    unittest.main()
