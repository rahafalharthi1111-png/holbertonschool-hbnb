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

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model("Place", {
    "title": fields.String(
        required=True,
        min_length=1,
        max_length=100,
        description="Title of the place (1-100 chars)"
    ),
    "description": fields.String(
        required=False,
        max_length=500,
        description="Description of the place (max 500 chars)"
    ),
    "price": fields.Float(
        required=True,
        description="Price of the place (must be positive)"
    ),
    "latitude": fields.Float(
        required=True,
        description="Latitude of the place (-90 to 90)"
    ),
    "longitude": fields.Float(
        required=True,
        description="Longitude of the place (-180 to 180)"
    ),
    "owner_id": fields.String(
        required=True,
        description="ID of the user who owns this place"
    ),
    "amenities": fields.List(
        fields.String,
        required=False,
        description="List of amenity IDs associated with this place"
    )
})

place_update_model = api.model("PlaceUpdate", {
    "title": fields.String(
        required=False, 
        min_length=1, 
        max_length=100
        ),
    "description": fields.String(
        required=False, 
        max_length=500
        ),
    "price": fields.Float(
        required=False
        ),
    "latitude": fields.Float(required=False ),
    "longitude": fields.Float(required=False),
    "amenities": fields.List(fields.String, required=False)
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

        result = place.to_dict(detailed=True)

        return result, 200

    @api.expect(place_update_model)
    @api.response(200, "Place updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(404, "Place not found")
    def put(self, place_id):
        data = request.get_json()
        
        place, error = facade.update_place(place_id, data)
        if error:
            return {"error": "Place not found or invalid data"}, 400
        
        return {"message": "Place was successfully updated"}, 200



@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [r.to_dict() for r in reviews], 200
