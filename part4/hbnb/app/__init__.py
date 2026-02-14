from fileinput import filename
from flask import Flask, app, send_from_directory
import config
from app.extensions import rest_api, bcrypt, jwt, db, CORS

def create_app(config_class=config.DevelopmentConfig):
    
    app = Flask(__name__)
    @app.route("/hbnb/frontend/static/<path:filename>")
    def serve_image(filename):
        return send_from_directory("/hbnb/frontend/static/", filename)
    app.config.from_object(config_class)

    app.url_map.strict_slashes = False
    

    CORS(app, resources={r"/api/v1/*": {"origins": "*"}}, supports_credentials=True, allow_headers="*")
    

    
    db.init_app(app)
    rest_api.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    



    
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
