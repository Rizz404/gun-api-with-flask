from flask import request, Blueprint, jsonify

from gundevilapp.app import db
from gundevilapp.users.models import User

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/')
def index():
  users = User.query.all()
  
  # * Ada function untuk ubah ke dict
  users_list = [user.to_dict() for user in users]
  
  return users_list

@users.route('/create', methods=['POST'])
def create():
  username = request.form.get('username') 
  email = request.form.get('email') 
  password = request.form.get('password') 
  role = request.form.get('role') 
  picture = request.form.get('picture') 
  bio = request.form.get('bio') 
  
  try:
    user = User(username= username, email=email, password=password, role=role, bio=bio, picture=picture)
    
    db.session.add(user)
    db.session.commit()
    
    user_dict = user.to_dict()
    
    return jsonify(user_dict), 201
  except Exception as e:
    return jsonify(str(e)), 500