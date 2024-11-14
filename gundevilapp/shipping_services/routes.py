from flask import request, Blueprint

from gundevilapp.app import db
from gundevilapp.shipping_services.models import ShippingService
from flask_login import login_required

from ..utils import api_response

shipping_services = Blueprint(
    'shipping_services', __name__, template_folder='templates')
