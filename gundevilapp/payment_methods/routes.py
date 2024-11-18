from flask import request, Blueprint

from gundevilapp.app import db
from gundevilapp.payment_methods.models import PaymentMethod
from flask_login import login_required

from ..utils import api_response

payment_methods = Blueprint(
    'payment_methods', __name__, template_folder='templates')


def parse_payment_method_data(data):
  return {
      'name': data.get('name'),
      'description': data.get('description'),
      'payment_method_fee': int(data.get('payment_method_fee')) if data.get('payment_method_fee') else None,
  }


@payment_methods.route('/', methods=['POST'])
@login_required
def create():
  try:
    payment_method_body = request.get_json() if request.is_json else request.form
    payment_method_data = parse_payment_method_data(payment_method_body)

    required_fields = ['name', 'description', 'payment_method_fee']
    missing_fields = [
      field for field in required_fields if not payment_method_data.get(field)]
    if missing_fields:
      return api_response.error(
        message="Missing required fields",
        code=400,
        errors=missing_fields
      )

    payment_method = PaymentMethod(**payment_method_data)
    db.session.add(payment_method)

    db.session.commit()
    return api_response.success(
      data=payment_method.to_dict(),
      message='Payment method created successfully',
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


@payment_methods.route('/', methods=['GET'])
def get_payment_methods():
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  payment_methods_query = PaymentMethod.query.all()

  return api_response.paginate(
      query=payment_methods_query,
      page=page,
      page_size=page_size
    )


@payment_methods.route('/<int:id>', methods=['GET'])
def get_payment_method_by_id(id):
  payment_method = PaymentMethod.query.get(id)

  if not payment_method:
    return api_response.error(
      message='Payment method not found',
      code=404,
      errors=payment_method
    )

  return api_response.success(
    data=payment_method.to_dict()
  )


@payment_methods.route('/<int:id>', methods=['PATCH', 'DELETE'])
@login_required
def update_and_delete_payment_method_by_id(id):
  payment_method = PaymentMethod.query.get(id)

  if not payment_method:
    return api_response.error(
      message='Payment method not found',
      code=404,
      errors=payment_method
    )

  if request.method == 'PATCH':
    try:
      payment_method_body = request.get_json() if request.is_json else request.form
      payment_method_data = parse_payment_method_data(payment_method_body)

      for key, value in payment_method_data.items():
        if value is not None:
          setattr(payment_method, key, value)

      db.session.commit()
      return api_response.success(
        message="Success update payment_method",
        data=payment_method.to_dict(),
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
      for picture in payment_method.pictures:
        db.session.delete(picture)

      db.session.delete(payment_method)
      db.session.commit()

      return api_response.success(
        message=f"Successfully delete payment method with id:{id}"
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
