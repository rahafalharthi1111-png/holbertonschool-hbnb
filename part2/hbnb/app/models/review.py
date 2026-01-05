from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Review text is required.")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        if not isinstance(place, Place):
            raise ValueError("Place must be exists.")
        if not isinstance(user, User):
            raise ValueError("User must be exists.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
