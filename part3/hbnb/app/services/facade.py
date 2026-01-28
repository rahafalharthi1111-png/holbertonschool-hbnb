from uuid import UUID

from app.persistence import (SQLAlchemyRepository, UserRepository,
PlaceRepository, ReviewRepository, AmenityRepository)
from app.models import User, Amenity, Place, Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

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
        
        user.user_update(data)

        self.user_repo.update(user.id, {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    })
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
        return self.amenity_repo.update(amenity_id, amenity_data)



    ## Places CRUD
    def create_place(self, place_data):

        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            return None


        amenities_objs = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                return None
            amenities_objs.append(amenity)

        try:
            place = Place(
                title=place_data["title"],
                description=place_data.get("description"),
                price=place_data["price"],
                latitude=place_data["latitude"],
                longitude=place_data["longitude"],
                user_id=owner.id
            )
            place.amenities = amenities_objs

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
            return None, "Place Not found"

        if "owner_id" in place_data:
            return None, "Owner cannot be updated"

        for field in ["title", "description", "price", "latitude", "longitude"]:
            if field in place_data:
                setattr(place, field, place_data[field])


        if "amenities" in place_data:
            amenities_objs = []
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    return None, f"Amenity {amenity_id} not found"
                amenities_objs.append(amenity)


            place.amenities = amenities_objs

        self.place_repo.commit()

        return place, None


    ## Reviwes CRUD
    def create_review(self, review_data, current_user_id):

        user = self.user_repo.get(current_user_id)
        if not user:
            raise ValueError("User not found.")
        
        place_id = review_data.get("place_id")
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        
        if place.owner.id == current_user_id:
            raise ValueError("Cannot review your own place")
        
        for review in place.reviews:
            if review.user_id == current_user_id:
                raise ValueError("You have already reviwed this place")

        text = review_data.get("text")
        rating = review_data.get("rating")
        if not text or rating is None:
            raise ValueError("All fields are required.")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        review = Review(text=text, rating=rating, user_id=user.id, place_id=place.id)
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

    def update_review(self, review_id, review_data, current_user_id):
        review = self.get_review(review_id)
        if not review:
            return None, "Reviwe not found."
        
        if review.user_id != current_user_id:
            return None, "Unauthorized action."

        if "text" in review_data:
            review.text = review_data["text"]

        if "rating" in review_data:
            rating = review_data["rating"]
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            review.rating = rating

        self.review_repo.update(review.id, review_data)
        return review, None

    def delete_review(self, review_id, current_user_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False, "Review not found."

        if review.user_id != current_user_id:
            return False, "Unauthorized action."
        
        place = review.place
        if review in place.reviews:
            place.reviews.remove(review)


        self.review_repo.delete(review.id)
        return True, None

    #admin CRUD
    def admin_update_user(self, user_id, email=None, password=None):
        user = self.get_user(user_id)
        if not user:
            return False, "User not found"
        
        if email:
            user.email = email
        if password:
            user.set_password(password)
        
        self.user_repo.save(user)
        return True, None
    
    def admin_create_user(self, user_data):
        email = user_data.get("email")
        password = user_data.get("password")
        first_name = user_data.get("first_name", "")
        last_name = user_data.get("last_name", "")
        is_admin = user_data.get("is_admin", False)

        if not email or not password:
            raise ValueError("Email and password are required.")

        if self.get_user_by_email(email):
            raise ValueError("Email already registered")


        user = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )

        self.user_repo.add(user)
        return user

    
    def admin_update_user(self, user_id, update_data):
        user = self.get_user(user_id)
        if not user:
            return None, "User not found."
        

        if "email" in update_data and update_data['email']:
            email = update_data['email']
            existing_user = self.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return None, "Email already in use."
        
        try:
            user.user_update(update_data)
            if 'password' in update_data and update_data['password']:
                user.hash_password(update_data['password'])
        except ValueError as e:
            return None, str(e)

        self.user_repo.update(user.id,{
            "email": user.email,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name
        })

        return user, None
    
    
    def admin_create_amenity(self, data):
        name = data.get("name")
        if not name or not name.strip():
            return None, "Amenity name is required."

        existing = self.amenity_repo.get_by_attribute("name", name.strip())
        if existing:
            return None, "Amenity already exists."

        amenity = Amenity(name=name.strip())
        self.amenity_repo.add(amenity)
        return amenity, None
    
    
    def admin_update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None, "Amenity not found"

        if 'name' in amenity_data and amenity_data['name'].strip():
            amenity.name = amenity_data['name'].strip()
        else:
            return None, "Amenity name is required"

        self.amenity_repo.update(amenity.id, {"name": amenity.name})
        return amenity, None


    def admin_update_place(self, place_id, place_data, bypass_owner=False):
        place = self.place_repo.get(place_id)
        if not place:
            return None, "Place not found"

        if not bypass_owner and "owner_id" in place_data:
            return None, "Owner cannot be updated"

        for field in ["title", "description", "price", "latitude", "longitude"]:
            if field in place_data:
                setattr(place, field, place_data[field])


        if "amenities" in place_data:
            amenities_objs = []
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    return None, f"Amenity {amenity_id} not found"
                amenities_objs.append(amenity)


            place.amenities = amenities_objs

        self.place_repo.commit()

        return place, None
