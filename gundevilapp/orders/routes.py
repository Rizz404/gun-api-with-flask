from flask import request, Blueprint

from gundevilapp.app import db
from gundevilapp.orders.models import Order
from flask_login import login_required

from ..utils import api_response

orders = Blueprint('orders', __name__, template_folder='templates')
