from flask import request, Blueprint

from gundevilapp.app import db
from gundevilapp.transactions.models import Transaction
from flask_login import login_required, current_user

from ..utils import api_response

transactions = Blueprint(
    'transactions', __name__, template_folder='templates')


def parse_transaction_data(data):
  return {
    'buyer_id': int(data.get('buyer_id')) if data.get('buyer_id') else None,
    'payment_method_id': int(data.get('payment_method_id')) if data.get('payment_method_id') else None,
    'admin_fee': int(data.get('admin_fee')) if data.get('admin_fee') else None,
    'shipping_service_fee': int(data.get('shipping_service_fee')) if data.get('shipping_service_fee') else None,
    'payment_method_fee': int(data.get('payment_method_fee')) if data.get('payment_method_fee') else None,
    'sub_total': int(data.get('sub_total')) if data.get('sub_total') else None,
    'total': int(data.get('total')) if data.get('total') else None,
    'payment_status': data.get('payment_status'),
  }


@transactions.route('/', methods=['POST'])
@login_required
def create():
  try:
    transaction_body = request.get_json() if request.is_json else request.form
    transaction_data = parse_transaction_data(transaction_body)

    transaction_data['buyer_id'] = current_user.id
    transaction_data['total'] = transaction_data['sub_total'] + \
        transaction_data['admin_fee'] + transaction_data['shipping_service_fee'] + \
        transaction_data['payment_method_fee']

    required_fields = [
        'payment_method_id',
        'admin_fee',
        'shipping_service_fee',
        'payment_method_fee',
        'sub_total',
    ]
    missing_fields = [
      field for field in required_fields if not transaction_data.get(field)]
    if missing_fields:
      return api_response.error(
        message="Missing required fields",
        code=400,
        errors=missing_fields
      )

    transactions = Transaction(**transaction_data)
    db.session.add(transactions)

    db.session.commit()
    return api_response.success(
      data=transactions.to_dict(),
      message='Transaction created successfully',
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


@transactions.route('/', methods=['GET'])
def get_transactions():
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  transactions_query = Transaction.query

  return api_response.paginate(
      query=transactions_query,
      page=page,
      page_size=page_size
    )


@transactions.route('/<int:id>', methods=['GET'])
def get_payment_method_by_id(id):
  transactions = Transaction.query.get(id)

  if not transactions:
    return api_response.error(
      message='Transaction not found',
      code=404,
      errors=transactions
    )

  return api_response.success(
    data=transactions.to_dict()
  )


@transactions.route('/<int:id>', methods=['PATCH', 'DELETE'])
@login_required
def update_and_delete_payment_method_by_id(id):
  transactions = Transaction.query.get(id)

  if not transactions:
    return api_response.error(
      message='Transaction not found',
      code=404,
      errors=transactions
    )

  if request.method == 'PATCH':
    try:
      transaction_body = request.get_json() if request.is_json else request.form
      transaction_data = parse_transaction_data(transaction_body)

      for key, value in transaction_data.items():
        if value is not None:
          setattr(transactions, key, value)

      db.session.commit()
      return api_response.success(
        message="Success update transactions",
        data=transactions.to_dict(),
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
      db.session.delete(transactions)
      db.session.commit()

      return api_response.success(
        message=f"Successfully delete transaction with id:{id}"
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
