from app.extensions import db
from app.models.base_model import BaseModel

class Review(BaseModel, db.Model):
    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
