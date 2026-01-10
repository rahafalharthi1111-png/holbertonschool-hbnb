from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

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
