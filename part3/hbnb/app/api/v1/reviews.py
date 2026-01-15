from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        current_user_id = get_jwt_identity()
        review_data = request.get_json()

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == current_user_id:
            return {"error": "You cannot review your own place"}, 400

        existing_review = facade.get_review_by_user_and_place(current_user_id, review_data['place_id'])
        if existing_review:
            return {"error": "You have already reviewed this place"}, 400

        review_data['user_id'] = current_user_id
        new_review = facade.create_review(review_data)
        return new_review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200


    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json()
        updated_review = facade.update_review(review_id, data)
        return updated_review.to_dict(), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
    
    
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review: Only the owner can delete"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        deleted = facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
