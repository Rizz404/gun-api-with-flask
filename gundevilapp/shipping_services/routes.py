from flask import request, Blueprint

from gundevilapp.app import db
from gundevilapp.shipping_services.models import ShippingService
from flask_login import login_required

from ..utils import api_response

shipping_services = Blueprint(
    'shipping_services', __name__, template_folder='templates')


def parse_shipping_service_data(data):
  return {
      'name': data.get('name'),
      'description': data.get('description'),
      'shipping_service_fee': int(data.get('shipping_service_fee')) if data.get('shipping_service_fee') else None,
      'estimation_time': data.get('estimation_time'),
  }


@shipping_services.route('/', methods=['POST'])
@login_required
def create():
  try:
    shipping_service_body = request.get_json() if request.is_json else request.form
    shipping_service_data = parse_shipping_service_data(shipping_service_body)

    required_fields = ['name', 'description', 'shipping_service_fee']
    missing_fields = [
      field for field in required_fields if not shipping_service_data.get(field)]
    if missing_fields:
      return api_response.error(
        message="Missing required fields",
        code=400,
        errors=missing_fields
      )

    shipping_service = ShippingService(**shipping_service_data)
    db.session.add(shipping_service)

    db.session.commit()
    return api_response.success(
      data=shipping_service.to_dict(),
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


@shipping_services.route('/', methods=['GET'])
def get_shipping_services():
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  shipping_services_query = ShippingService.query

  return api_response.paginate(
      query=shipping_services_query,
      page=page,
      page_size=page_size
    )


@shipping_services.route('/<int:id>', methods=['GET'])
def get_shipping_service_by_id(id):
  shipping_service = ShippingService.query.get(id)

  if not shipping_service:
    return api_response.error(
      message='Payment method not found',
      code=404,
      errors=shipping_service
    )

  return api_response.success(
    data=shipping_service.to_dict()
  )


@shipping_services.route('/<int:id>', methods=['PATCH', 'DELETE'])
@login_required
def update_and_delete_shipping_service_by_id(id):
  shipping_service = ShippingService.query.get(id)

  if not shipping_service:
    return api_response.error(
      message='Payment method not found',
      code=404,
      errors=shipping_service
    )

  if request.method == 'PATCH':
    try:
      shipping_service_body = request.get_json() if request.is_json else request.form
      shipping_service_data = parse_shipping_service_data(shipping_service_body)

      for key, value in shipping_service_data.items():
        if value is not None:
          setattr(shipping_service, key, value)

      db.session.commit()
      return api_response.success(
        message="Success update shipping_service",
        data=shipping_service.to_dict(),
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
      db.session.delete(shipping_service)
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
