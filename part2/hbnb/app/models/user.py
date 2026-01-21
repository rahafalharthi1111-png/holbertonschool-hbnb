from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name[:50].strip()
        self.last_name = last_name[:50].strip()
        self.email = email.lower()
        self.is_admin = is_admin

        self.validate()

    def validate(self):
        # validate that first name is not empty or " "
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name is required")

        # validate that last name is not empty or " "
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name is required")

        # validate that the email match emails patterns
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email):
            raise ValueError("Invalid email format")
        
    def user_update(self, data):
        if 'first_name' in data:
            self.first_name = data['first_name'][:50].strip()
        if 'last_name' in data:
            self.last_name = data['last_name'][:50].strip()
        if 'email' in data:
            self.email = data['email'].lower().strip()
        self.validate()
