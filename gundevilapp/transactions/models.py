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
  buyer_id = db.Column(db.Integer, db.ForeignKey(
    'users.id'), nullable=False)  # Foreign Key untuk pembeli
  seller_id = db.Column(db.Integer, db.ForeignKey(
    'users.id'), nullable=False)  # Foreign Key untuk penjual
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

  def to_dict(self, include_relationships=None):
    data = {
      'id': self.id,
      'buyer_id': self.buyer_id,
      'seller_id': self.seller_id,
      'payment_method_id': self.payment_method_id,
      'admin_fee': self.admin_fee,
      'shipping_service_fee': self.shipping_service_fee,
      'payment_method_fee': self.payment_method_fee,
      'sub_total': self.sub_total,
      'total': self.total,
      'payment_status': self.payment_status,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }

    if include_relationships:
      for relationship in include_relationships:
        match relationship:
          case 'seller':
            data["seller"] = self.seller.to_dict(
            ) if self.seller.to_dict() else None
          case 'buyer':
            data["buyer"] = self.buyer.to_dict(
            ) if self.buyer.to_dict() else None
          case 'payment_method':
            data["payment_method"] = self.payment_method.to_dict(
            ) if self.payment_method.to_dict() else None
          case 'orders':
            data['orders'] = [transaction.to_dict()
                              for transaction in self.orders]

    return data
