#!/usr/bin/python3
"""
Place module.

This module defines two classes: BaseModel and Place.
- BaseModel provides basic ID and timestamp functionality.
- Place represents a rental place, with validations on title, price,
  location, and relationships with amenities and reviews.
"""

import uuid
from datetime import datetime

from app.models.amenity import Amenity
from app.models.user import User


class BaseModel:
    """
    Base model class providing ID, created_at, and updated_at fields.
    """

    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id if id else str(uuid.uuid4())
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()

    def save(self):
        self.updated_at = datetime.utcnow()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()


class Place(BaseModel):
    """
    Represents a place available for rental.
    """

    def __init__(
        self,
        id=None,
        owner=None,
        title=None,
        description=None,
        price=0.0,
        latitude=0.0,
        longitude=0.0,
        created_at=None,
        updated_at=None
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        self.owner = owner

        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if len(title) > 100:
            raise ValueError("title must contain a maximum of 100 characters")
        self.title = title

        if description is not None and not isinstance(description, str):
            raise TypeError("description must be a string")
        self.description = description

        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if price < 0:
            raise ValueError("price must be greater than or equal to 0")
        self.price = round(float(price), 2)

        if not isinstance(latitude, (int, float)):
            raise TypeError("latitude must be a number")
        if not -90 <= latitude <= 90:
            raise ValueError("latitude must be between -90 and 90")
        self.latitude = round(float(latitude), 1)

        if not isinstance(longitude, (int, float)):
            raise TypeError("longitude must be a number")
        if not -180 <= longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")
        self.longitude = round(float(longitude), 1)

        # Relationships
        self.amenities = []  # list of Amenity IDs or objects (handled elsewhere)
        self.reviews = []    # list of Review IDs ONLY

    def add_amenity(self, amenity):
        """
        Adds an Amenity to the place.
        """
        if isinstance(amenity, Amenity) and amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        """
        Serializes the Place object to a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "owner_id": self.owner.id if self.owner else None,
            "amenities": [
                amenity.to_dict() for amenity in self.amenities
            ],
            "reviews": self.reviews  # list of review IDs
        }

