from uuid import uuid4
from datetime import datetime

class Review:
    def __init__(self, text, user_id, place_id):
        if not text:
            raise ValueError("Review text is required")

        self.id = str(uuid4())
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update(self, text):
        if not text:
            raise ValueError("Review text is required")

        self.text = text
        self.updated_at = datetime.utcnow()
