from app import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

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


    def hash_password(self, password):
        if not password:
            raise ValueError("Password is required")
        
        from app.extensions import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


    def verify_password(self, password):
        from app.extensions import bcrypt
        return bcrypt.check_password_hash(self.password, password)
