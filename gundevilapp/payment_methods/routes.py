from flask import request, Blueprint

from gundevilapp.app import db
from gundevilapp.payment_methods.models import PaymentMethod
from flask_login import login_required

from ..utils import api_response

payment_methods = Blueprint(
    'payment_methods', __name__, template_folder='templates')
