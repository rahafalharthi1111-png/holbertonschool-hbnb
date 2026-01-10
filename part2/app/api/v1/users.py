from flask_restx import Namespace, Resource, fields
from app.services import facade

# تعريف الـNamespace
api = Namespace('users', description='User operations')

# نموذج User (لـAPI documentation)
user_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Resource example (اختياري حتى لا يعطي خطأ عند تشغيل السيرفر)
@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        result = [user.to_dict() for user in users]
        return result, 200
