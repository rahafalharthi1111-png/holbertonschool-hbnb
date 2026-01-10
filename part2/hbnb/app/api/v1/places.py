from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace("places", description="Place operations")

amenity_model = api.model("PlaceAmenity", {
    "id": fields.String,
    "name": fields.String
})

user_model = api.model("PlaceUser", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String
})

place_model = api.model("Place", {
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenities": fields.List(fields.String)
})


@api.route("/")
class PlaceList(Resource):

    @api.expect(place_model)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        data = request.get_json()
        place = facade.create_place(data)
        if not place:
            return {"error": "Invalid input data"}, 400
        return place.to_dict(), 201

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200


@api.route("/<place_id>")
class PlaceResource(Resource):

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)
        amenities = [facade.get_amenity(a) for a in place.amenities]

        result = place.to_dict()
        result["owner"] = owner.to_dict() if owner else None
        result["amenities"] = [a.to_dict() for a in amenities if a]

        return result, 200

    @api.expect(place_model)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    def put(self, place_id):
        data = request.get_json()
        place = facade.update_place(place_id, data)
        if not place:
            return {"error": "Place not found or invalid data"}, 404
        return {"message": "Place updated successfully"}, 200
