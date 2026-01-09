import unittest
from app import app


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_create_amenity_success(self):
        response = self.client.post("/api/v1/amenities", json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_missing_name(self):
        response = self.client.post("/api/v1/amenities", json={})
        self.assertEqual(response.status_code, 400)

    def test_get_amenities(self):
        response = self.client.get("/api/v1/amenities")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
