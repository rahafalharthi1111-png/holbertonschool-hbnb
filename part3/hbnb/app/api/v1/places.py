from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenities": fields.List(fields.String),
    "reviews": fields.List(fields.Nested(review_model), description="List of reviews")
})


@api.route("/")
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        data['owner_id'] = current_user_id
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

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(403, "Unauthorized action")
    def put(self, place_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json()
        updated_place = facade.update_place(place_id, data)
        return updated_place.to_dict(), 200



@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [r.to_dict() for r in reviews], 200
