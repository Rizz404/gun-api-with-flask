from flask import request, Blueprint, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from ..utils import api_response

from gundevilapp.app import db, bcrypt
from gundevilapp.users.models import User, RoleEnum
from gundevilapp.users.routes import parse_user_data

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['POST'])
def register():
  try:
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role', 'user')

    if not username or not email or not password:
      return api_response.error(
        message="Username, email, and passwor are required",
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
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    if not username or not password:
      return api_response.error(
        message="Username and password are required",
        code=400
      )

    user = User.query.filter(User.username == username).first()

    if bcrypt.check_password_hash(user.password, password):
      login_user(user, remember=remember)
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


@auth.route('/profile', methods=['GET'])
@login_required
def get_user_profile():
  user_data = {
      "id": current_user.id,
      "username": current_user.username,
      "email": current_user.email
  }
  return api_response.success(
    data=user_data
  )
