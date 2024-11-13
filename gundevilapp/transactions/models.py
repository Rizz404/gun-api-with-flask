import enum
from gundevilapp.app import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class PaymentStatusEnum(enum.Enum):
  PENDING = "PENDING"
  COMPLETED = "COMPLETED"
  FAILED = "FAILED"


class Transaction(db.Model):
  __tablename__ = 'transactions'

  id = db.Column(db.Integer, primary_key=True)
  buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  payment_method_id = db.Column(
    db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
  admin_fee = db.Column(db.Integer, nullable=False, default=0)
  shipping_service_fee = db.Column(db.Integer, nullable=False, default=0)
  payment_method_fee = db.Column(db.Integer, nullable=False, default=0)
  sub_total = db.Column(db.Integer, nullable=False, default=0)
  total = db.Column(db.Integer, nullable=False, default=0)
  payment_status = db.Column(
    db.Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING)
  created_at = db.Column(db.DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(
    timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  # * Relasi
  buyer = relationship("User", foreign_keys=[
                       buyer_id], back_populates="transactions_bought")
  seller = relationship("User", foreign_keys=[
                        seller_id], back_populates="transactions_sold")
  payment_method = relationship("PaymentMethod", back_populates="transactions")
  orders = relationship("Order", back_populates="transaction")

  def __repr__(self):
    return f"<Transaction id: {self.id}>"

  def get_id(self):
    return self.id
