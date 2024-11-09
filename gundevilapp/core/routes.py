from flask import request, Blueprint

from gundevilapp.app import db

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
def index():
  return "it's work"