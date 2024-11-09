from flask_login import UserMixin
from app import db

# * Pake sqlite type datanya terbates hati-hati
class User(db.username, UserMixin):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, nullable=False)
  email = db.Column(db.Text, nullable=False)
  password = db.Column(db.Text, nullable=False)
  role = db.Column(db.Text)
  picture = db.Column(db.Text)
  bio = db.Column(db.Text)
  
  def __repr__(self):
    return f"<User: {self.username} and Role: {self.role}>"
  
  def get_id(self):
    return self.id
  
  def to_dict(self):
    return{
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "password": self.password,
      "role": self.role,
      "picture": self.picture,
      "bio": self.bio,
    }