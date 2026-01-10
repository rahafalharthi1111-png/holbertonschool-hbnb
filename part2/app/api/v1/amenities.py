from flask_restx import Namespace, Resource, fields
from app.services import facade

# تعريف الـNamespace
api = Namespace('amenities', description='Amenity operations')

# نموذج Amenity (لـAPI documentation)
amenity_model = api.model('Amenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# Resource example (اختياري حتى لا يعطي خطأ عند تشغيل السيرفر)
@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        result = [amenity.to_dict() for amenity in amenities]
        return result, 200
