from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()


def create_app():
  app = Flask(__name__, template_folder='templates')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./gun.db'

  # * Waktu session login
  app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

  # * Nanti taro di env
  app.secret_key = os.getenv('secret_key')

  db.init_app(app)

  # * Harus di init di sini lib nya
  bcrypt.init_app(app)
  cors.init_app(app)

  login_manager = LoginManager()
  login_manager.init_app(app)

  from gundevilapp.users.models import User

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(id)

  from gundevilapp.core.routes import core
  from gundevilapp.auth.routes import auth
  from gundevilapp.guns.routes import guns
  from gundevilapp.users.routes import users
  from gundevilapp.cart.routes import cart

  # * Nanti tinggal tambahin kalo mau ada routes lain
  app.register_blueprint(core, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/auth')
  app.register_blueprint(guns, url_prefix='/guns')
  app.register_blueprint(users, url_prefix='/users')
  app.register_blueprint(cart, url_prefix='/cart')

  migrate = Migrate(app, db)

  return app
