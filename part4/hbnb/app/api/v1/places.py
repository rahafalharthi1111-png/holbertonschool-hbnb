from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

ns = Namespace("places", description="Place operations")

facade = HBnBFacade()

amenity_model = ns.model("PlaceAmenity", {
    "id": fields.String,
    "name": fields.String
})

user_model = ns.model("PlaceUser", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String
})

review_model = ns.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = ns.model("Place", {
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
    "image": fields.String(
        required=False,
        description="URL of the place image"
    ),
    "owner_id": fields.String(
        required=True,
        description="ID of the user who owns this place"
    ),
    "amenities": fields.List(
        fields.String,
        required=False,
        description="List of amenity IDs associated with this place",

    )
})

place_update_model = ns.model("PlaceUpdate", {
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
    "owner_id": fields.String(
        required=True,
        description="ID of the user who owns this place",
        
    ),
    "amenities": fields.List(fields.String, required=False)
})


place_resp_model = ns.model("PlaceResponse", {
    "id": fields.String,
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,

    "owner_id": fields.String(attribute="user_id"),
    "image": fields.String,
    "amenities": fields.List(
        fields.String,
        attribute=lambda place: [amenity.name for amenity in place.amenities]
    )
})



@ns.route("/")
class PlaceList(Resource):
    @jwt_required()
    @ns.expect(place_model)
    @ns.response(201, "Place successfully created")
    @ns.response(400, "Invalid input data")
    def post(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        data["owner_id"] = current_user

        place = facade.create_place(data)

        return place.to_dict(), 201

    @ns.response(200, "List of places retrieved successfully")
    def get(self):
        places = facade.get_all_places()
        return ns.marshal(places, place_resp_model), 200


@ns.route("/<place_id>")
class PlaceResource(Resource):

    @ns.response(200, "Place details retrieved successfully")
    @ns.response(404, "Place not found")
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner_id = facade.get_user(place.user_id)
        amenities = place.amenities

        

        return ns.marshal(place, place_resp_model), 200
    
    
    @jwt_required()
    @ns.expect(place_update_model)
    @ns.response(200, "Place updated successfully")
    @ns.response(400, "Invalid input data")
    @ns.response(403, "Unauthorized action")
    @ns.response(404, "Place not found")
    def put(self, place_id):
        current_user = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner is None or place.owner.id != current_user:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json() or {}
        if "owner_id" in data:
            return {"error": "Cannot update owner_id"}, 400

        updated_place, error = facade.update_place(place_id, data)
        if error:
            return {"error": "Place not found or invalid data"}, 400

        return {"message": "Place was successfully updated"}, 200




@ns.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @ns.response(200, 'List of reviews for the place retrieved successfully')
    @ns.response(404, 'Place not found')
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return ns.marshal(reviews, review_model), 200
