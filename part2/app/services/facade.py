from app.models.review import Review

class HBnBFacade:

    def create_review(self, text, user_id, place_id):
        user = self.get_user(user_id)
        place = self.get_place(place_id)

        if not user or not place:
            raise ValueError("User or Place not found")

        review = Review(text, user_id, place_id)
        self.storage.save(review)

        place.reviews.append(review.id)

        return review

    def get_review(self, review_id):
        return self.storage.get("Review", review_id)

    def update_review(self, review_id, text):
        review = self.get_review(review_id)
        if not review:
            return None

        review.update(text)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False

        place = self.get_place(review.place_id)
        if place and review_id in place.reviews:
            place.reviews.remove(review_id)

        self.storage.delete(review)
        return True

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None

        return [self.get_review(rid) for rid in place.reviews]
