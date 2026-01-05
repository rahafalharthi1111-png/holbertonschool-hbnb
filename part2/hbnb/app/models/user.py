from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name[:50]
        self.last_name = last_name[:50]
        self.email = email
        self.is_admin = is_admin

        self.validate()

    def validate(self):
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are required")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email):
            raise ValueError("Invalid email format")
