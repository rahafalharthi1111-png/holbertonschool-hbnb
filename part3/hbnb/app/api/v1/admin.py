from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt

from app.services.facade import HBnBFacade

ns = Namespace('admin', description='Admin operations')

facade = HBnBFacade()

admin_user_model = ns.model("AdminUserCreate", {
    "email": fields.String(required=True, description="User email, must be unique"),
    "password": fields.String(required=True, description="User password"),
    "first_name": fields.String(required=True, description="User first name"),
    "last_name": fields.String(required=True, description="User last name"),
    "is_admin": fields.Boolean(required=True, description="Whether the user is an admin")
})

admin_resp_user_model = ns.model('AdminRespUserModel',{
    "id": fields.String,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "is_admin": fields.Boolean
})

user_update_model = ns.model("AdminUserUpdate", {
    "email": fields.String(required=False, description="New email address"),
    "password": fields.String(required=False, description="New password"),
    "first_name": fields.String(required=False, description="New first name"),
    "last_name": fields.String(required=False, description="New last name"),
})

amenity_model = ns.model("AmenityCreate", {
    "name": fields.String(required=True, description="Name of the amenity")
})

place_update_model = ns.model("AdminPlaceUpdate", {
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
        description="ID of the user who owns this place"
    ),
    "amenities": fields.List(fields.String, required=False)
})

@ns.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @ns.expect(user_update_model)
    @ns.response(200, 'User updated successfully')
    @ns.response(403, 'Admin privileges required')
    @ns.response(404, 'Email is already in use')
    def put(self, user_id):
        current_user = get_jwt()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        try:
            success, error = facade.admin_update_user(user_id, data)
            if error:
                return {'error': error}, 400
            return {"message": "User updated successfully"}, 200
        except ValueError as e:
            return {'error': str(e)}, 400


@ns.route("/users/")
class AdminUserCreate(Resource):
    @jwt_required()
    @ns.expect(admin_user_model)
    @ns.response(400, "Email already registered or invalid input")
    @ns.response(403, "Admin privileges required")
    def post(self):
        current_user = get_jwt()
        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        user_data = request.get_json()
        try:
            user = facade.admin_create_user(user_data)
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    

@ns.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @ns.expect(user_update_model)
    @ns.response(200, "User updated successfully")
    @ns.response(400, "Invalid input data")
    @ns.response(403, "Admin privileges required")
    @ns.response(404, "User not found")
    def put(self, user_id):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json or {}

        updated_user, error = facade.admin_update_user(user_id, data)
        
        if error:
            if error == "User not found.":
                return {"error": error}, 404
            if error == "Email already in use.":
                return {"error": error}, 400

        return {"message": "User updated successfully"}, 200


@ns.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @ns.expect(amenity_model)
    @ns.response(201, "Amenity created successfully")
    @ns.response(400, "Invalid input data")
    @ns.response(403, "Admin privileges required")
    def post(self):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json or {}
        name = data.get("name")
        if not name:
            return {"error": "Name is required"}, 400

        amenity, error = facade.admin_create_amenity(data)
        
        if error:
            return {"error": error}, 400

        return {"message": "Amenity created successfully", "amenity": amenity.to_dict()}, 201


@ns.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @ns.expect(amenity_model)
    def put(self, amenity_id):
        current_user = get_jwt()
        
        if not current_user.get('is_admin'):
            return {"error": "Admin privileges required"}, 403


        amenity_data = request.get_json()

        amenity, error = facade.admin_update_amenity(amenity_id, amenity_data)


        if error:
            if error == "Amenity not found":
                return {"error": error}, 404
            return {"error": error}, 400

        return amenity.to_dict(), 200
    
@ns.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    @ns.expect(place_update_model)
    def put(self, place_id):
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner.id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()

        updated_place, error = facade.admin_update_place(place_id, data, bypass_owner=is_admin)

        if error:
            return {"error": error}, 400

        return updated_place.to_dict(), 200
