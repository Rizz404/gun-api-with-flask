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

  if os.getenv('VERCEL_ENV') == 'production':
    # * Konfigurasi SSL yang lebih aman
    database_url = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'ssl': {
              'ca': '../ca-certificate.crt',  # * Path ke file CA certificate
              'ssl_mode': 'REQUIRED'
            }
        }
    }
  else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./gun.db'

  # * Waktu session login
  app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

  # * Nanti taro di env
  app.secret_key = os.getenv('SECRET_KEY')

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
  from gundevilapp.sales.routes import sales

  # * Nanti tinggal tambahin kalo mau ada routes lain
  app.register_blueprint(core, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/auth')
  app.register_blueprint(guns, url_prefix='/guns')
  app.register_blueprint(users, url_prefix='/users')
  app.register_blueprint(cart, url_prefix='/cart')
  app.register_blueprint(sales, url_prefix='/sales')

  migrate = Migrate(app, db)

  return app
