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
