from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name[:50]
        self.last_name = last_name[:50]
        self.email = email
        self.is_admin = is_admin

        self.password = None
        self.hash_password(password)


        self.validate()

    def validate(self):
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are required")
        
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email):
            raise ValueError("Invalid email format")
    

    def hash_password(self, password):
        if not password:
            raise ValueError("Password is required")
        
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
    

    def to_dict(self):
        data = super().to_dict()
        data.pop("password", None)
        return data
