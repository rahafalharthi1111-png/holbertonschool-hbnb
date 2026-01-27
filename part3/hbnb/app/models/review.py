from app.models.base_model import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__= "reviews"

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    #Foreign Keys
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String, db.ForeignKey('places.id'), nullable=False)

    
    @validates('text')
    def validate_text(self, key, value):
        if not value or not value.strip():
            raise ValueError("Review text is required.")
        return value.strip()
    
    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value
    
    @validates('user_id')
    def validate_user(self, key, value):
        from app.models.user import User
        user = User.query.get(value)
        if not user:
            raise ValueError("User must be exists.")
        return value
    
    @validates('place_id')
    def validate_place(self, key, value):
        from app.models.place import Place
        place = Place.query.get(value)
        if not Place:
            raise ValueError("Place must be exists.")
        return value
