import unittest
from app import app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.valid_place = {
            "name": "Nice Apartment",
            "owner_id": "1234",
            "price_per_night": 150
        }

    def test_create_place_success(self):
        response = self.client.post("/api/v1/places", json=self.valid_place)
        self.assertEqual(response.status_code, 201)

    def test_create_place_missing_name(self):
        data = {
            "owner_id": "1234",
            "price_per_night": 150
        }
        response = self.client.post("/api/v1/places", json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_places(self):
        response = self.client.get("/api/v1/places")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
