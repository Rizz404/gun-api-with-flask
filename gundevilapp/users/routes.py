from flask import request, Blueprint, jsonify
from flask_login import current_user, login_required

from gundevilapp.app import db
from gundevilapp.users.models import User

users = Blueprint('users', __name__, template_folder='templates')


def parse_user_data(data, is_form=False):
  if is_form:
    return {
        'username': data.get('username'),
        'email': data.get('email'),
        'password': data.get('password'),
        'role': data.get('role'),
        'picture': data.get('picture'),
        'bio': data.get('bio'),
    }
  return {
      'username': data.get('username'),
      'email': data.get('email'),
      'password': data.get('password'),
      'role': data.get('role'),
      'picture': data.get('picture'),
      'bio': data.get('bio'),
  }


@users.route('/')
def index():
  users = User.query.all()

  # * Ada function untuk ubah ke dict
  users_list = [user.to_dict() for user in users]

  return users_list


@users.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def with_id(id):
  user = User.query.get(id)

  if not user:
    return jsonify({"error": "Gun not found"}), 404

  if request.method == 'GET':
    return jsonify(user.to_dict())

  elif request.method == 'DELETE':
    try:
      db.session.delete(user)
      db.session.commit()
      return jsonify({
        'message': f'User with id {id} successfully deleted'
      })
    except Exception as e:
      db.session.rollback()
      return jsonify(str(e)), 500


@users.route('/profile', methods=['GET'])
@login_required
def get_user_profile():
  user_data = {
      "id": current_user.id,
      "username": current_user.username,
      "email": current_user.email
  }
  return jsonify(user_data), 200
