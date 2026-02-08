from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import authorizations

ns = Namespace('users', description='User operations')

facade = HBnBFacade()

# Define the user model for input validation and documentation
user_create_model = ns.model('UserCreate', {
    'first_name': fields.String(
        required=True,
        min_length=1,
        max_length=50,
        description='User first name'),
    'last_name': fields.String(
        required=True,
        min_length=1,
        max_length=50,
        description='User last name'),
    'email': fields.String(
        required=True, 
        description='User email',
        example='use@example.com'),
    'password': fields.String(
        required=True,
        min_length=8,
        description='User passsword'
    )
})

user_update_model = ns.model('UserUpdate', {
    'first_name': fields.String(
        required=False,
        min_length=1,
        max_length=50,
        description='User first name'),
    'last_name': fields.String(
        required=False,
        min_length=1,
        max_length=50,
        description='User last name'),
    'email': fields.String(
        required=False, 
        description='User email',
        example='use@example.com'),
    'password': fields.String(
        required=False,
        min_length=8,
        description='User passsword'
    )
})

user_resp_model = ns.model('User_resp',{
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String
})

@ns.route('/')
class UserList(Resource):
    @ns.expect(user_create_model, validate=True)
    @ns.response(201, 'User successfully created')
    @ns.response(400, 'Email already registered')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = ns.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)},400
        
        return {
            'id': new_user.id,
            'message': 'User successfuly created'
            }, 201
    
    
    def get(self):
        """Retrieve list of all users"""
        users = facade.get_all_users()
        resp = ns.marshal(users, user_resp_model)
        return [ user for user in resp], 200


@ns.route('/<user_id>')
class UserResource(Resource):
    @ns.response(200, 'User details retrieved successfully')
    @ns.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return ns.marshal(user, user_resp_model), 200

    @jwt_required()
    @ns.doc(security='BearerAuth')
    @ns.expect(user_update_model, validate=True)
    @ns.response(400, 'Email already registered')
    @ns.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user information"""
        claims = get_jwt()
        current_user = get_jwt_identity()
        data = ns.payload
        print(get_jwt_identity())
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        is_admin = claims.get('is_admin', False)

        if not is_admin:
            if user_id != current_user:
                return{'error': 'Unauthorized action'}, 403
            if 'email' in data or 'password' in data:
                return{'error': 'Cannot modify email or password'}, 400
            
        if is_admin and 'email' in data:
            existing = facade.get_user_by_email(data['email'])
            if existing and existing.id != user_id:
                return{'error': 'Email already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
        except ValueError as e:
            return{'error': str(e)}, 400
        return ns.marshal(updated_user, user_resp_model), 200
