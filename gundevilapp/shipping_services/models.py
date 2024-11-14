from gundevilapp.app import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class ShippingService(db.Model):
  __tablename__ = 'shipping_services'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  description = db.Column(db.Text)
  estimation_time = db.Column(db.String, nullable=False)
  shipping_service_fee = db.Column(db.Integer, nullable=False, default=0)
  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(
    timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  # Relasi ke Order
  orders = relationship("Order", back_populates="shipping_service")

  def __repr__(self):
    return f"<Shipping service id: {self.id}>"

  def get_id(self):
    return self.id
