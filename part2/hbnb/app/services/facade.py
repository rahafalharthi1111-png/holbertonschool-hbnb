from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    #Users CRUD
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        
        for key, value in data.items():
            setattr(user, key, value)
        self.user_repo.update(user.id, data)
        return user
    
    
    #Amenity CRUD
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")

        if not name:
            return None

        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)

        return amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            return None

        name = amenity_data.get("name")
        if not name:
            return False

        amenity.name = name
        return amenity



    ## Places CRUD
    def create_place(self, place_data):

        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            return None


        amenities_ids = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                return None
            amenities_ids.append(amenity.id)

        try:
            place = Place(
                title=place_data["title"],
                description=place_data.get("description"),
                price=place_data["price"],
                latitude=place_data["latitude"],
                longitude=place_data["longitude"],
                owner=owner
            )

            for amenity in amenities_ids:
                 place.add_amenity(amenity)

        except Exception as e:
            print("Place creation error:", e)
            return None

        self.place_repo.add(place)
        return place
        
    def get_place(self, place_id):
        return self.place_repo.get(place_id)


    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        try:
            place.update(place_data)
            self.place_repo.update(place.id, place_data)
            return place
        except Exception:
            return None



     ## Reviwes CRUD

    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        text = review_data.get("text")
        rating = review_data.get("rating")

        if not user_id or not place_id or not text or rating is None:
            raise ValueError("All fields (user_id, place_id, text, rating) are required.")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found.")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        review = Review(text=text, rating=rating, user=user, place=place)
        self.review_repo.add(review)
        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        if "text" in review_data:
            review.text = review_data["text"]
        if "rating" in review_data:
            rating = review_data["rating"]
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            review.rating = rating

        self.review_repo.update(review.id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False

        self.review_repo.delete(review.id)
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        return True
