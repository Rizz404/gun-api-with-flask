from flask import request, Blueprint, jsonify

from gundevilapp.app import db
from gundevilapp.guns.models import Gun

guns = Blueprint('guns', __name__, template_folder='templates')

@guns.route('/')
def index():
  guns = Gun.query.all()
  
  # * Ada function untuk ubah ke dict
  guns_list = [gun.to_dict() for gun in guns]
  
  return guns_list

@guns.route('/create', methods=['POST'])
def create():
  model = request.form.get('model') 
  caliber = request.form.get('caliber') 
  capacity = request.form.get('capacity') 
  length = request.form.get('length') 
  weight = request.form.get('weight') 
  action = request.form.get('action') 
  price = request.form.get('price') 
  
  try:
    gun = Gun(model= model, caliber=caliber, capacity=capacity, length=length, weight=weight, action=action, price=price)
    
    db.session.add(gun)
    db.session.commit()
    
    gun_dict = gun.to_dict()
    
    return jsonify(gun_dict), 201
  except Exception as e:
    return jsonify(str(e)), 500