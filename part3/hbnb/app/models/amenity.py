from app.extensions import db
from app.models.base_model import BaseModel

class Amenity(BaseModel, db.Model):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False, unique=True)
