from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity


ns = Namespace('reviews', description='Review operations')

facade = HBnBFacade()

review_model = ns.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@ns.route('/')
class ReviewList(Resource):
    @jwt_required()
    @ns.expect(review_model)
    @ns.response(201, 'Review successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            review = facade.create_review(data, current_user)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@ns.route('/<review_id>')
class ReviewResource(Resource):
    @ns.response(200, 'Review details retrieved successfully')
    @ns.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @jwt_required()
    @ns.expect(review_model)
    @ns.response(200, 'Review updated successfully')
    @ns.response(404, 'Review not found')
    @ns.response(400, 'Invalid input data')
    @ns.response(403, 'Unauthorized action')
    def put(self, review_id):
        data = request.get_json()
        current_user_id = get_jwt_identity()

        review, error = facade.update_review(review_id, data, current_user_id)

        if error:
            if error == "Unauthorized action.":
                return{"error": error}, 403
            elif error == "Reviwe not found.":
                return {"error": error}, 404
            else:
                return {"error": error}, 400
        return{"message": "Review updated successfully"}, 200

    @jwt_required()
    @ns.response(200, 'Review deleted successfully')
    @ns.response(404, 'Review not found')
    @ns.response(403, 'Unauthorized action')
    def delete(self, review_id):
        current_user_id = get_jwt_identity()

        success, error = facade.delete_review(review_id, current_user_id)
        
        if error:
            if error == "Review not found.":
                return {"error": error}, 404
            if error == "Unauthorized action.":
                return{"error": error}, 403
            
        return {"message": "Review deleted successfully."}, 200
