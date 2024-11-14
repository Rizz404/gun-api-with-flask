from flask import request, Blueprint, jsonify
from flask_login import current_user, login_required
from ..utils import api_response

from gundevilapp.app import db
from gundevilapp.users.models import User

users = Blueprint('users', __name__, template_folder='templates')


def parse_user_data(data):
  # * Deteksi apakah data berbentuk dict (kemungkinan dari JSON) atau ImmutableMultiDict (dari form)
  if isinstance(data, dict):  # * JSON input (request.get_json())
    return {
        'username': data.get('username'),
        'email': data.get('email'),
        'password': data.get('password'),
        'role': data.get('role'),
        'picture': data.get('picture'),  # nullable
        'bio': data.get('bio'),  # nullable
    }
  else:  # * Form input (request.form)
    return {
        'username': data.get('username', None),
        'email': data.get('email', None),
        'password': data.get('password', None),
        'role': data.get('role', None),
        'picture': data.get('picture', None),  # nullable
        'bio': data.get('bio', None),  # nullable
    }


@users.route('/')
def get_users():
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  users_query = User.query

  return api_response.paginate(users_query, page, page_size)


@users.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
  user = User.query.get(id)

  if not user:
    return api_response.error(
      message="User not found",
      code=404
    )

  return api_response.success(
    data=user.to_dict()
  )


@users.route('/<int:id>', methods=['PATCH', 'DELETE'])
@login_required
def update_and_delete_user_by_id(id):
  user = User.query.get(id)

  if not user:
    return api_response.error(
      message="User not found",
      code=404
    )

  if request.method == 'PATCH':
    try:
      if request.is_json:
        user_data = parse_user_data(request.get_json())
      else:
        user_data = parse_user_data(request.form)

      for key, value in user_data.items():
        if value is not None:
          setattr(user, key, value)

      db.session.commit()
      return api_response.success(
          message=f"Successfully updated user with id:{id}",
          data=user.to_dict()
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


@users.route('/profile', methods=['GET', 'PATCH'])
@login_required
def get_and_update_user_profile():
  user = User.query.get(current_user.id)

  if not user:
    return api_response.error(
      message="User not found",
      code=404
    )

  if request.method == 'GET':
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
  elif request.method == 'PATCH':
    try:
      if request.is_json:
        user_data = parse_user_data(request.get_json())
      else:
        user_data = parse_user_data(request.form)

      for key, value in user_data.items():
        if value is not None:
          setattr(user, key, value)

      db.session.commit()
      return api_response.success(
          message=f"Successfully updated profile",
          data=user.to_dict()
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
