from app.extensions import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
import re

class User(BaseModel):
    __tablename__ = "users"

    #Columns
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    #Relastionships
    places = db.relationship("Place", backref='owner', lazy=True)
    reviews = db.relationship("Review", backref='auth', lazy=True)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name.strip()[:50]
        self.last_name = last_name.strip()[:50]
        self.email = email.lower().strip()
        self.is_admin = is_admin
        self.hash_password(password)


    @validates("first_name")
    def validate_first_name(self, key, value):
        # validate that first name is not empty or " "
        value = value[:50].strip()
        if not value:
            raise ValueError("First name is required.")
        return value
    
    @validates("last_name")
    def validate_last_name(self, key, value):
        # validate that last name is not empty or " "
        value = value[:50].strip()
        if not value:
            raise ValueError("Last name is required.")
        return value

    @validates("email")
    def validate_email(self, key, value):
        # validate that the email match emails patterns
        value = value.lower().strip()
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError("Invalid email format.")
        return value


    def hash_password(self, password):
        if not password:
            raise ValueError("Password is required")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


    def user_update(self, data):
        for field in ["first_name", "last_name", "email"]:
            if field in data:
                setattr(self, field, data[field])
