from flask import request, Blueprint, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from ..utils import api_response

from gundevilapp.app import db, bcrypt
from gundevilapp.users.models import User, RoleEnum
from gundevilapp.users.routes import parse_user_data

auth = Blueprint('auth', __name__, template_folder='templates')


def parse_auth_data(data):
  return {
    'username': data.get('username'),
    'email': data.get('email'),
    'password': data.get('password'),
    'role': data.get('role'),
  }


@auth.route('/register', methods=['POST'])
def register():
  try:
    auth_body = request.get_json() if request.is_json else request.form
    auth_data = parse_auth_data(auth_body)

    # * Desctrcuture caranya kek gini guys
    username, email, password, role = auth_data.values()

    if not username or not email or not password:
      return api_response.error(
        message="Username, email, and password are required",
        code=400
      )

    user = User.query.filter(User.username == username,
                             User.email == email).first()

    existing_user = User.query.filter(
        or_(User.username == username, User.email == email)
     ).first()

    if existing_user:
      return api_response.error(
          message="Username or email already taken",
          code=400
        )

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    role_enum = RoleEnum(role.lower()) if role.lower() in [
        'user', 'admin'] else RoleEnum.USER

    user = User(username=username, email=email,
                password=hashed_password, role=role_enum)

    db.session.add(user)
    db.session.commit()
    return api_response.success(
      data=user.to_dict(),
      code=201
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


@auth.route('/login', methods=['POST'])
def login():
  try:
    auth_body = request.get_json() if request.is_json else request.form
    auth_data = parse_auth_data(auth_body)

    username, password = auth_data['username'], auth_data['password']

    if not username or not password:
      return api_response.error(
        message="Username, password and password are required",
        code=400
      )

    user = User.query.filter(User.username == username).first()

    if not user:
      return api_response.error(
          message="User not found",
          code=404
      )

    if bcrypt.check_password_hash(user.password, password):
      login_user(user, remember=True)
      return api_response.success(
        message=f"Welcome {user.username}!",
        data=user.to_dict()
      )
    else:
      return api_response.error(
        message="Invalid username or password",
        code=401
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


@auth.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return api_response.success(
    message="Logout successfull"
  )
