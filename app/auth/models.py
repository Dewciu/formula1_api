from app.database import db
from app.auth import bcrypt
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username: str, email: str, password: str) -> None:
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password_hash = str(
            bcrypt.generate_password_hash(password).decode("utf-8")
        )

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash.encode("utf-8"), password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
