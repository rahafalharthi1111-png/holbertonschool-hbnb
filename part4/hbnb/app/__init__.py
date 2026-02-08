from flask import Flask
import config
from app.extensions import rest_api, bcrypt, jwt, db, CORS





def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    rest_api.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)

    
    from app.api.v1.users import ns as users_ns
    from app.api.v1.amenities import ns as amenities_ns
    from app.api.v1.places import ns as places_ns
    from app.api.v1.reviews import ns as reviews_ns
    from app.api.v1.login import ns as login_ns
    from app.api.v1.admin import ns as admin_ns

    # Register the namespace

    rest_api.add_namespace(users_ns, path='/api/v1/users')
    rest_api.add_namespace(amenities_ns, path='/api/v1/amenities')
    rest_api.add_namespace(places_ns, path="/api/v1/places")
    rest_api.add_namespace(reviews_ns, path="/api/v1/reviews")
    rest_api.add_namespace(login_ns, path= '/api/v1/auth')
    rest_api.add_namespace(admin_ns, path='/api/v1/admin')
    

    return app
