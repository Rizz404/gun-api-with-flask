from gundevilapp.app import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class PaymentMethod(db.Model):
  __tablename__ = 'payment_methods'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  description = db.Column(db.Text)
  payment_method_fee = db.Column(db.Integer, nullable=False, default=0)
  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(
    timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  transactions = relationship("Transaction", back_populates="payment_method")

  def __repr__(self):
    return f"<Payment Method id: {self.id}>"

  def get_id(self):
    return self.id
