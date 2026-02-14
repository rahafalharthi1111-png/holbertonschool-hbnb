from sqlalchemy.orm import validates

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.extensions import db

#Association table for Place <-> Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = "places"

    #Columns
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    #Foreign Key to User (owner)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)

    #Column for image URL
    image = db.Column(db.String(255), nullable=True)

    #Relationships
    reviews = db.relationship("Review", backref="place", lazy=True)
    amenities = db.relationship("Amenity", secondary=place_amenity, backref=db.backref("places", lazy=True))
    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value) > 100:
            raise ValueError("Title is required and max 100 chars.")
        return value.strip()
    
    @validates('price')
    def validate_price(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Price must be positive.")
        return float(value)
    
    @validates('latitude')
    def validate_latitude(self, key, value):
        if value is None or value < -90 or value >90:
            raise ValueError("Latitude must be between -90 and 90")
        return float(value)
    
    @validates('longitude')
    def validate_longitude(self, key, value):
        if value is None or value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return float(value)


    def to_dict(self, detailed=False):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None,
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [amenity.id for amenity in self.amenities],
            "image": self.image
        }
        if detailed:
            data["owner"] = self.owner.to_dict() if self.owner else None
            data["amenities"] = [amenity.to_dict() for amenity in self.amenities] 
        return data
