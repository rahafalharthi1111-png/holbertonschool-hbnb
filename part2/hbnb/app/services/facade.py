from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

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
        from app.models.amenity import Amenity
from app.services.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.amenity_repo = InMemoryRepository()

    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        if not name:
            raise ValueError("Amenity name is required")

        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        name = amenity_data.get("name")
        if not name:
            raise ValueError("Amenity name is required")

        amenity.name = name
        return amenity

        if not user:
            return None
        
        for key, value in data.items():
            setattr(user, key, value)
        self.user_repo.update(user.id, data)
        return user
    
    def get_place(self, place_id):
        return self.place_repo.get(place_id)
