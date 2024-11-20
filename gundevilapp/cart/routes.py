from flask import request, Blueprint, jsonify
from flask_login import login_required, current_user

from ..utils import api_response

from gundevilapp.app import db
from gundevilapp.cart.models import Cart, CartItems

cart = Blueprint('cart', __name__, template_folder='templates')


def parse_cart_data(data, is_form=False):
  # * Helper function buat parse data buat form dan juga json
  if is_form:
    return {
      'user_id': data.get('user_id'),
    }
  return {
    'user_id': data.get('user_id'),
  }


def parse_cart_item_data(data, is_form=False):
  # * Helper function buat parse data buat form dan juga json
  if is_form:
    return {
      "cart_id": int(data.get('cart_id')) if data.get('cart_id') else None,
      "gun_id": int(data.get('gun_id')) if data.get('gun_id') else None,
      "quantity": int(data.get('quantity')) if data.get('quantity') else 0,
    }
  return {
    "cart_id": data.get('cart_id'),
    "gun_id": data.get('gun_id'),
    "quantity": data.get('quantity', 0),
  }


@cart.route('/', methods=['GET', 'POST'])
@login_required
def index():
  if request.method == 'GET':
    cart = Cart.query.filter_by(user_id=current_user.id).first()

    return api_response.success(
      data=cart.to_dict(),
    )
  elif request.method == 'POST':
    try:
      if request.is_json:
        data = request.get_json()
        cart_data = parse_cart_data(data)
      else:
        cart_data = parse_cart_data(request.form, is_form=True)

      # * Gunakan current_user.id untuk user_id
      cart_data['user_id'] = current_user.id

      existing_cart = Cart.query.filter_by(user_id=current_user.id).first()

      if existing_cart:
        return api_response.error(message="Cart already created")

      cart = Cart(**cart_data)
      db.session.add(cart)
      db.session.commit()
      return api_response.success(
        data=cart.to_dict(),
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


@cart.route('/<int:id>', methods=['GET', 'DELETE'])
def with_id(id):
  cart = Cart.query.get(id)

  if not cart:
    return api_response.error(
      message="Cart not found",
      code=404
    )

  if request.method == 'GET':
    return api_response.success(
      data=cart.to_dict()
    )

  elif request.method == 'DELETE':
    try:
      db.session.delete(cart)
      db.session.commit()

      return api_response.success(
        message=f'Cart with id {id} successfully deleted'
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


@cart.route('/cart-items/', methods=['GET', 'POST'])
def cart_items():
  if request.method == 'GET':
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    cart = Cart.query.filter_by(user_id=current_user.id).first()

    cart_items = CartItems.query.filter_by(cart_id=cart.id)

    return api_response.paginate(
      query=cart_items,
      page=page,
      page_size=page_size,
    )
  elif request.method == 'POST':
    try:
      if request.is_json:
        data = request.get_json()
        cart_item_data = parse_cart_item_data(data)
      else:
        cart_item_data = parse_cart_item_data(request.form, is_form=True)

      required_fields = ['cart_id', 'gun_id']
      missing_fields = [
        field for field in required_fields if not cart_item_data.get(field)]
      if missing_fields:
        return api_response.error(
          message="Missing required fields",
          errors=missing_fields
        )

      cart_item = CartItems(**cart_item_data)
      db.session.add(cart_item)
      db.session.commit()

      return api_response.success(
        data=cart_item.to_dict(),
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


@cart.route('/cart-items/<int:id>', methods=['PATCH', 'DELETE'])
def cart_items_with_id(id):
  cart_item = CartItems.query.get(id)

  if not cart_item:
    return api_response.error(
      message="Cart item not found",
      code=404
    )

  if request.method == 'PATCH':
    try:
      if request.is_json:
        data = request.get_json()
        cart_item_data = parse_cart_item_data(data)
      else:
        cart_item_data = parse_cart_item_data(request.form, is_form=True)

      if cart_item_data.get('gun_id'):
        cart_item.gun_id = cart_item_data['gun_id']
      if cart_item_data.get('quantity'):
        cart_item.quantity = cart_item_data['quantity']

      db.session.commit()

      return api_response.success(
        message="Cart item updated sucessfully",
        data=cart_item.to_dict()
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

  elif request.method == 'DELETE':
    try:
      db.session.delete(cart_item)
      db.session.commit()

      return api_response.success(
        message=f'CartItem with id {id} successfully deleted'
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
