from sqlalchemy.orm import validates

from app.models import BaseModel
from app.extensions import db



class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False)

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Amenity name is required and max 50 chars.")
        return value
