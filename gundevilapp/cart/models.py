from gundevilapp.app import db
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Cart(db.Model):
  __tablename__ = 'cart'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey(
    'users.id'), nullable=False, unique=True)  # * unique=True untuk one-to-one
  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(
    timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  # * Relasi ke CartItems (One-to-Many)
  cart_items = relationship(
    "CartItems", back_populates="cart", cascade="all, delete-orphan")
  user = relationship("User", back_populates="cart")

  def __repr__(self):
    return f"<Cart: {self.id}, User: {self.user_id}>"

  def get_id(self):
    return self.id

  def to_dict(self, include_relationships=None):
    data = {
      "id": self.id,
      "user_id": self.user_id,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }

    if include_relationships:
      for relationship in include_relationships:
        match relationship:
          case 'user':
            data["user"] = self.user.to_dict(
            ) if self.user.to_dict() else None
          case 'cart_items':
            data['cart_items'] = [cart_item.to_dict()
                                  for cart_item in self.cart_items]
    return data


class CartItems(db.Model):
  __tablename__ = 'cart_items'

  id = db.Column(db.Integer, primary_key=True)
  cart_id = db.Column(db.Integer, ForeignKey('cart.id'), nullable=False)
  gun_id = db.Column(db.Integer, ForeignKey('guns.id'), nullable=False)
  quantity = db.Column(db.Integer, nullable=False,
                       default=0)  # * Jumlah quantity
  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(
    timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  # * Relasi back-reference ke model Cart
  cart = relationship("Cart", back_populates="cart_items")
  gun = relationship("Gun", back_populates="cart_items")

  def __repr__(self):
    return f"<Cart items: {self.id}, gun_id: {self.gun_id}>"

  def get_id(self):
    return self.id

  def to_dict(self, include_relationships=None):
    data = {
      'id': self.id,
      'cart_id': self.cart_id,
      'gun_id': self.gun_id,
      'quantity': self.quantity,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }

    if include_relationships:
      for relationship in include_relationships:
        match relationship:
          case 'cart':
            data["cart"] = self.cart.to_dict(
            ) if self.cart.to_dict() else None
          case 'gun':
            data["gun"] = self.gun.to_dict(
            ) if self.gun.to_dict() else None

    return data
