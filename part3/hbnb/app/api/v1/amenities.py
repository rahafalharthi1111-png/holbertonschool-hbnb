from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

ns = Namespace('amenities', description='Amenity operations')

facade = HBnBFacade()


amenity_model = ns.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_resp_model = ns.model("AmenityResponse",{
    'id': fields.String,
    'name': fields.String,
})


@ns.route('/')
class AmenityList(Resource):

    @ns.expect(amenity_model)
    @ns.response(201, 'Amenity successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = ns.payload
        amenity = facade.create_amenity(data)

        if not amenity:
            return {"error": "Invalid input data"}, 400

        
        return ns.marshal(amenity, amenity_resp_model), 201

    @ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()
        return ns.marshal(amenities, amenity_resp_model), 200
    


@ns.route('/<amenity_id>')
class AmenityResource(Resource):

    @ns.response(200, 'Amenity details retrieved successfully')
    @ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return ns.marshal(amenity, amenity_resp_model), 200

    @ns.expect(amenity_model)
    @ns.response(200, 'Amenity updated successfully')
    @ns.response(404, 'Amenity not found')
    @ns.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity"""
        data = ns.payload
        result = facade.update_amenity(amenity_id, data)

        if result is None:
            return {"error": "Amenity not found"}, 404
        if result is False:
            return {"error": "Invalid input data"}, 400

        return {"message": "Amenity updated successfully"}, 200
