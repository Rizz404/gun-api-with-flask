from gundevilapp.app import db

class Gun(db.Model):
  __tablename__ = 'guns'
  
  id = db.Column(db.Integer, primary_key=True)
  model = db.Column(db.Text)
  caliber = db.Column(db.Integer)
  capacity = db.Column(db.Integer)
  length = db.Column(db.Integer)
  weight = db.Column(db.Integer)
  action = db.Column(db.Text)
  price = db.Column(db.Integer)
  
  def __repr__(self):
    return f"<Gun: {self.model}, Price: {self.price}>"
  
  def get_id(self):
    return self.id
  
  def to_dict(self):
    return{
      "id": self.id,
      "model": self.model,
      "caliber": self.caliber,
      "capacity": self.capacity,
      "length": self.length,
      "weight": self.weight,
      "action": self.action,
      "price": self.price,
    }
