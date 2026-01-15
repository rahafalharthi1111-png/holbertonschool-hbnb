from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


facade = HBnBFacade()
api = Namespace('users', description='User operations')


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password')
})

# User update model (exclude email and password)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        claims = get_jwt()

        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(data)
        return user.to_dict(), 201

@api.route('/<user_id>')
class UserResource(Resource):

    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200


    @jwt_required()
    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Cannot modify email or password')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        data = api.payload or {}

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        is_admin = claims.get('is_admin', False)


        if not is_admin:
            if user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            if 'email' in data or 'password' in data:
                return {'error': 'Cannot modify email or password'}, 400

        if is_admin and 'email' in data:
            existing = facade.get_user_by_email(data['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        return updated_user.to_dict(), 200
