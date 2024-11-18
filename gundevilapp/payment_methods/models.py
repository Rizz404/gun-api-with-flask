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

  def to_dict(self, include_relationships=None):
    data = {
      'name': self.name,
      'description': self.description,
      'payment_method_fee': self.payment_method_fee,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }

    if include_relationships:
      for relationship in include_relationships:
        match relationship:
          case 'transactions':
            data['transactions'] = [transaction.to_dict()
                                    for transaction in self.transactions]

    return data
