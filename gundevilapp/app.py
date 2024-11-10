from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
  app = Flask(__name__, template_folder='templates')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./gun.db'

  db.init_app(app)

  # * Harus di init di sini lib nya
  bcrypt.init_app(app)

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

  # * Nanti tinggal tambahin kalo mau ada routes lain
  app.register_blueprint(core, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/auth')
  app.register_blueprint(guns, url_prefix='/guns')
  app.register_blueprint(users, url_prefix='/users')

  migrate = Migrate(app, db)

  return app
