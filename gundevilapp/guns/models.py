import enum
from gundevilapp.app import db
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Gun(db.Model):
  __tablename__ = 'guns'
  
  id = db.Column(db.Integer, primary_key=True)
  model = db.Column(db.String(100), nullable=False)
  caliber = db.Column(db.Integer, nullable=False)
  capacity = db.Column(db.Integer, nullable=False)
  length = db.Column(db.Integer, nullable=True)
  weight = db.Column(db.Integer, nullable=True)
  action = db.Column(db.String(100), nullable=False)
  price = db.Column(db.Integer, nullable=False)
  description = db.Column(db.Text, nullable=True)  # * Penjelasan senjata
  stock = db.Column(db.Integer, nullable=False, default=0)  # * Jumlah stok
  
  # * Timestamps
  created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))  
  
  # * Relasi ke GunPictures (One-to-Many)
  pictures = relationship("GunPictures", back_populates="gun", cascade="all, delete-orphan")
  
  def __repr__(self):
    return f"<Gun: {self.model}, Price: {self.price}>"
  
  def get_id(self):
    return self.id
  
  def to_dict(self):
    return{
      "id": self.id,
      "model": self.model,
      "caliber": self.caliber,
      "capacity": self.capacity,
      "length": self.length,
      "weight": self.weight,
      "action": self.action,
      "price": self.price,
      "description": self.description,
      "stock": self.stock,
      "created_at": self.created_at.isoformat(),
      "updated_at": self.updated_at.isoformat(),
      "pictures": [picture.to_dict() for picture in self.pictures]  # Include related pictures
    }
    
class GunPictures(db.Model):
  __tablename__ = 'gun_pictures'

  id = db.Column(db.Integer, primary_key=True)
  gun_id = db.Column(db.Integer, ForeignKey('guns.id'), nullable=False)
  picture_url = db.Column(db.String(255), nullable=False)  # * URL gambar
  description = db.Column(db.String(255))  # * Optional keterangan gambar
  
  # * Relasi back-reference ke model Gun
  gun = relationship("Gun", back_populates="pictures")
  
  def __repr__(self):
    return f"<Gun picture: {self.picture_url}, description: {self.description}>"
  
  def get_id(self):
    return self.id
  
  def to_dict(self):
    return {
      "id": self.id,
      "picture_url": self.picture_url,
      "description": self.description
    }