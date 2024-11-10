from datetime import datetime, timezone
import enum
from flask_login import UserMixin
from gundevilapp.app import db

# * Pake sqlite type datanya terbates hati-hati


class RoleEnum(enum.Enum):
  USER = 'user'
  ADMIN = 'admin'


class User(db.Model, UserMixin):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, nullable=False)
  email = db.Column(db.Text, nullable=False)
  password = db.Column(db.Text, nullable=False)
  role = db.Column(db.Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
  picture = db.Column(db.Text)
  bio = db.Column(db.Text)

  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(
    timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  # * Relasi one-to-one ke Cart
  cart = db.relationship("Cart", back_populates="user",
                         uselist=False, cascade="all, delete-orphan")

  def __repr__(self):
    return f"<User: {self.username} and Role: {self.role}>"

  def get_id(self):
    return self.id

  def to_dict(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "password": self.password,
      "role": self.role.value,
      "picture": self.picture,
      "bio": self.bio,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
      "cart": self.cart.to_dict() if self.cart else None
    }
