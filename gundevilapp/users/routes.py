from flask import request, Blueprint, jsonify
from flask_login import current_user, login_required
from ..utils import api_response

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
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  users_query = User.query

  return api_response.paginate(users_query, page, page_size)


@users.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def with_id(id):
  user = User.query.get(id)

  if not user:
    return api_response.error(
      message="User not found",
      code=404
    )

  if request.method == 'GET':
    return api_response.success(
      data=user.to_dict()
    )

  elif request.method == 'DELETE':
    try:
      db.session.delete(user)
      db.session.commit()
      return api_response.success(
        message=f"Successfully delete user with id:{id}"
      )
    except ValueError as e:
      db.session.rollback()
      return api_response.error(message=str(e))
    except Exception as e:
      return api_response.error(
        message="Internal server error",
        code=500,
        errors=str(e)
      )


@users.route('/profile', methods=['GET'])
@login_required
def get_user_profile():
  user_data = {
      "id": current_user.id,
      "username": current_user.username,
      "email": current_user.email,
      "password": current_user.password,
      "role": current_user.role.value,
      "picture": current_user.picture,
      "bio": current_user.bio,
      "created_at": current_user.created_at,
      "updated_at": current_user.updated_at,
  }
  return api_response.success(
    data=user_data
  )
