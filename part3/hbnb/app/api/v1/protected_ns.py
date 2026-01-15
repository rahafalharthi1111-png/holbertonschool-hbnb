from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('protected_ns', description='Protected routes example')

@api.route('/')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()

        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        return {
            'message': f'Hello, user {current_user_id}',
            'is_admin': is_admin
        }, 200

