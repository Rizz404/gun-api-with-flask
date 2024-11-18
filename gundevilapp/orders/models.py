from gundevilapp.app import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Order(db.Model):
  __tablename__ = 'orders'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  gun_id = db.Column(db.Integer, db.ForeignKey('guns.id'), nullable=False)
  transaction_id = db.Column(
    db.Integer, db.ForeignKey('transactions.id'), nullable=False)
  shipping_service_id = db.Column(
    db.Integer, db.ForeignKey('shipping_services.id'), nullable=False)
  price_sold = db.Column(db.Integer, nullable=False, default=0)
  quantity = db.Column(db.Integer, nullable=False, default=1)
  total_price = db.Column(db.Integer, nullable=False, default=0)
  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(
    timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  # * Relasi
  user = relationship("User", back_populates="orders")
  gun = relationship("Gun", back_populates="orders")
  transaction = relationship("Transaction", back_populates="orders")
  shipping_service = relationship(
      "ShippingService", back_populates="orders")

  def __repr__(self):
    return f"<Order id: {self.id}>"

  def get_id(self):
    return self.id

  def to_dict(self, include_relationships=None):
    data = {
      'id': self.id,
      'user_id': self.user_id,
      'gun_id': self.gun_id,
      'transaction_id': self.transaction_id,
      'shipping_service_id': self.shipping_service_id,
      'price_sold': self.price_sold,
      'quantity': self.quantity,
      'total_price': self.total_price,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }

    if include_relationships:
      for relationship in include_relationships:
        match relationship:
          case "user":
            data["user"] = self.user.to_dict() if self.user else None
          case "gun":
            data["gun"] = self.gun.to_dict() if self.gun else None
          case "transaction":
            data["transaction"] = self.transaction.to_dict(
            ) if self.transaction else None
          case "shipping_service":
            data["shipping_service"] = self.shipping_service.to_dict(
            ) if self.shipping_service else None
          case _:
            pass

    return data
