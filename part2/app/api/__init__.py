from flask_restx import Api
from .v1.places import api as places_ns

api = Api(title="HBnB API", version="1.0")
api.add_namespace(places_ns, path='/api/v1/places')
