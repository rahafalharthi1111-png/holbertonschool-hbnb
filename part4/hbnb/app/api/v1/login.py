from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade

ns = Namespace("auth", description='Authintication operations')

facade = HBnBFacade()

# Model for input validation
login_model = ns.model('Login',{
    "email": fields.String(
        required=True,
        description='User emal'
    ),
    'password': fields.String(
        required=True,
        description='User password'
    )
})
@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    @ns.response(401, 'Invalid credentials')
    @ns.response(200, 'successfuly loged in')
    def post(self):
        credentials = ns.payload

        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )

        return {'access_token': access_token}, 200
