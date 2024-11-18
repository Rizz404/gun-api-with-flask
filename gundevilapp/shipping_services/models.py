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

  def to_dict(self, include_relationships=None):
    data = {
      'name': self.name,
      'description': self.description,
      'shipping_service_fee': self.shipping_service_fee,
      'estimation_time': self.estimation_time,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }

    if include_relationships:
      for relationship in include_relationships:
        match relationship:
          case 'oders':
            data['oders'] = [transaction.to_dict()
                             for transaction in self.oders]

    return data
