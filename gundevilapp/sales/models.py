from gundevilapp.app import db
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Sales(db.Model):
  __tablename__ = 'sales'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  gun_id = db.Column(db.Integer, db.ForeignKey('guns.id'),
                     nullable=True)  # Nullable for cart purchases
  total_amount = db.Column(db.Integer, nullable=False)  # Total payment
  quantity = db.Column(db.Integer, nullable=False, default=1)
  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(
    timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  # * Relasi ke User dan Gun
  user = relationship("User", back_populates="sales")
  gun = relationship("Gun", back_populates="sales")

  def __repr__(self):
    return f"<Sales: {self.id}, User: {self.user}, Amount: {self.total_amount}>"

  def get_id(self):
    return self.id

  def to_dict(self):
    return {
        "id": self.id,
        "user_id": self.user_id,
        "gun_id": self.gun_id,
        "total_amount": self.total_amount,
        "quantity": self.quantity,
        "created_at": self.created_at.isoformat(),
        "gun": self.gun.to_dict() if self.gun else None,
        "user": self.user.to_dict() if self.user else None,
    }
