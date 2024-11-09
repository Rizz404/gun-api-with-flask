from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
  app = Flask(__name__, template_folder='templates')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./gun.db'
  
  db.init_app(app)
  
  from gundevilapp.guns.routes import guns
  from gundevilapp.core.routes import core
  
  # * Nanti tinggal tambahin kalo mau ada routes lain
  app.register_blueprint(core, url_prefix='/')
  app.register_blueprint(guns, url_prefix='/guns')
  
  migrate = Migrate(app, db)
  
  return app