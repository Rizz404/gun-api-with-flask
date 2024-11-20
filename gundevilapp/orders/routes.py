from flask import request, Blueprint

from gundevilapp.app import db
from gundevilapp.orders.models import Order
from gundevilapp.shipping_services.models import ShippingService
from gundevilapp.guns.models import Gun
from flask_login import login_required, current_user

from ..utils import api_response

orders = Blueprint('orders', __name__, template_folder='templates')


def parse_order_data(data):
  return {
    'gun_id': int(data.get('gun_id')) if data.get('gun_id') else None,
    'transaction_id': int(data.get('transaction_id')) if data.get('transaction_id') else None,
    'shipping_service_id': int(data.get('shipping_service_id')) if data.get('shipping_service_id') else None,
    'price_sold': int(data.get('price_sold')) if data.get('price_sold') else None,
    'quantity': int(data.get('quantity')) if data.get('quantity') else None,
    'total_price': int(data.get('total_price')) if data.get('total_price') else None,
  }


@orders.route('/', methods=['POST'])
@login_required
def create():
  try:
    order_body = request.get_json() if request.is_json else request.form
    order_data = parse_order_data(order_body)
    shipping_service = ShippingService.query.get(
      order_data['shipping_service_id'])
    gun = Gun.query.get(order_data['gun_id'])

    order_data['user_id'] = current_user.id
    order_data['price_sold'] = gun.price
    order_data['total_price'] = gun.price * \
        order_data['quantity'] + shipping_service.shipping_service_fee

    required_fields = ['gun_id',
                       'transaction_id',
                       'shipping_service_id',
                       'quantity',
                       ]
    missing_fields = [
      field for field in required_fields if not order_data.get(field)]
    if missing_fields:
      return api_response.error(
        message="Missing required fields",
        code=400,
        errors=missing_fields
      )

    order = Order(**order_data)
    db.session.add(order)

    db.session.commit()
    return api_response.success(
      data=order.to_dict(include_relationships=[
                         'user', 'user', 'shipping_service', 'transaction']),
      message='Order created successfully',
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


@orders.route('/', methods=['GET'])
def get_orders():
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  orders_query = Order.query

  return api_response.paginate(
      query=orders_query,
      page=page,
      page_size=page_size
    )


@orders.route('/user/<int:id>', methods=['GET'])
def get_orders_by_user_id(id):
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  orders_query = Order.query.filter_by(user_id=id)

  return api_response.paginate(
      query=orders_query,
      page=page,
      page_size=page_size
    )


@orders.route('/<int:id>', methods=['GET'])
def get_order_by_id(id):
  order = Order.query.get(id)

  if not order:
    return api_response.error(
      message='Order not found',
      code=404,
      errors=order
    )

  return api_response.success(
    data=order.to_dict(include_relationships=[
        'user', 'user', 'shipping_service', 'transaction'])
  )
