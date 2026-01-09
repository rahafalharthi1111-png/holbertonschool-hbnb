import unittest
from app import app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.valid_review = {
            "user_id": "1234",
            "place_id": "5678",
            "text": "Great place!"
        }

    def test_create_review_success(self):
        response = self.client.post("/api/v1/reviews", json=self.valid_review)
        self.assertEqual(response.status_code, 201)

    def test_create_review_missing_text(self):
        data = {
            "user_id": "1234",
            "place_id": "5678"
        }
        response = self.client.post("/api/v1/reviews", json=data)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
