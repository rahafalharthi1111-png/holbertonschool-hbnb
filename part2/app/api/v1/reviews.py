"""
Module reviews.py
------------------

This module defines the RESTful API endpoints related to reviews
in the HBnB application.

Endpoints:
    - POST   /reviews/                     Create a new review
    - GET    /reviews/<review_id>          Get a review by ID
    - PUT    /reviews/<review_id>          Update a review
    - DELETE /reviews/<review_id>          Delete a review
    - GET    /reviews/places/<place_id>    Get all reviews for a place
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Review model (no rating in Part 2)
review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'text': fields.String(required=True, description='Text of the review'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    """
    Handles creation of reviews
    """

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new review
        """
        data = api.payload

        try:
            review = facade.create_review(
                data['text'],
                data['user_id'],
                data['place_id']
            )
        except Exception as e:
            api.abort(400, str(e))

        return {
            'id': review.id,
            'text': review.text,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 201


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    """
    Handles operations on a single review
    """

    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get a review by ID
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        return {
            'id': review.id,
            'text': review.text,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """
        Update a review
        """
        data = api.payload

        try:
            review = facade.update_review(review_id, data['text'])
        except Exception as e:
            api.abort(400, str(e))

        if not review:
            api.abort(404, 'Review not found')

        return {
            'id': review.id,
            'text': review.text,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review
        """
        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, 'Review not found')

        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<string:place_id>')
class PlaceReviewList(Resource):
    """
    Get all reviews for a specific place
    """

    @api.response(200, 'Reviews retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve all reviews for a place
        """
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            api.abort(404, 'Place not found')

        return [{
            'id': review.id,
            'text': review.text,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        } for review in reviews], 200
