from flask import request, Blueprint, jsonify

from gundevilapp.app import db
from gundevilapp.guns.models import Gun
from gundevilapp.sales.models import Sales
from ..utils import api_response
from flask_login import current_user, login_required

sales = Blueprint('sales', __name__, template_folder='templates')


def parse_sale_data(data, is_form=False):
  # * Helper function buat parse data buat form dan juga json
  if is_form:
    return {
      'gun_id': int(data.get('gun_id')) if data.get('gun_id') else None,
      'total_amount': data.get('total_amount') if data.get('total_amount') is not None else None,
      'quantity': int(data.get('quantity')) if data.get('quantity') else 1,
    }
  return {
    'gun_id': int(data.get('gun_id')),
    'total_amount': data.get('total_amount') if data.get('total_amount') is not None else None,
    'quantity': int(data.get('quantity')) if data.get('quantity') else 1,
  }


@sales.route('/', methods=['GET', 'POST'])
@login_required
def index():
  if request.method == 'GET':
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    sales_query = Sales.query
    return api_response.paginate(
        query=sales_query,
        page=page,
        page_size=page_size
    )
  elif request.method == 'POST':
    try:
      if request.is_json:
        data = request.get_json()
        sale_data = parse_sale_data(data)
      else:
        sale_data = parse_sale_data(request.form, is_form=True)

      user_id = current_user.id

      gun = Gun.query.get(sale_data['gun_id'])
      if not gun:
        return api_response.error(message="Gun not found", code=404)

      if gun.stock < sale_data['quantity']:
        return api_response.error(message="Not enough stock available", code=400)

      gun.stock -= sale_data['quantity']
      gun.sold_count += sale_data['quantity']
      total_amount = gun.price * sale_data['quantity']

      sale = Sales(
          user_id=user_id,
          gun_id=gun.id,
          total_amount=int(total_amount),
          quantity=sale_data['quantity']
      )

      db.session.add(sale)
      db.session.commit()

      return api_response.success(
          message="Sale created successfully",
          data=sale.to_dict(),
          code=201
      )

    except ValueError as e:
      db.session.rollback()
      return api_response.error(message=str(e))
    except Exception as e:
      db.session.rollback()
      return api_response.error(
          message="Internal server error",
          code=500,
          errors=str(e)
      )


@sales.route('/user', methods=['GET'])
@login_required
def sales_user():
  user_id = current_user.id
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  sales_query = Sales.query.filter_by(user_id=user_id)
  return api_response.paginate(
      query=sales_query,
      page=page,
      page_size=page_size
  )


@sales.route('/<int:id>', methods=['GET', 'DELETE'])
@login_required
def with_id(id):
  sale = Sales.query.get(id)

  if not sale:
    return api_response.error(
      message='Sales not found',
      code=404,
      errors=sale
    )

  if request.method == 'GET':
    return api_response.success(
      data=sale.to_dict()
    )

  elif request.method == 'DELETE':
    try:
      db.session.delete(sale)
      db.session.commit()

      return api_response.success(
        message=f"Successfully delete sale with id:{id}"
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
