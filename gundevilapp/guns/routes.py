from flask import request, Blueprint, jsonify

from gundevilapp.app import db
from gundevilapp.guns.models import Gun, GunPictures
from flask_login import login_required, current_user
# ? gak tau cara kerja importnya gimana, yang penting work
from ..utils import api_response

guns = Blueprint('guns', __name__, template_folder='templates')


def parse_gun_data(data):
  return {
    'model': data.get('model'),
    # * Untuk cegah yang int dikonversi kalo null
    'caliber': int(data.get('caliber')) if data.get('caliber') else None,
    'capacity': int(data.get('capacity')) if data.get('capacity') else None,
    'length': int(data.get('length')) if data.get('length') else None,
    'weight': int(data.get('weight')) if data.get('weight') else None,
    'action': data.get('action'),
    'price': int(data.get('price')) if data.get('price') else None,
    'description': data.get('description'),
    'stock': int(data.get('stock')) if data.get('stock') else None,
  }


def create_gun_pictures(gun, pictures_data):
  # * Helper function buat gun_pictures
  for picture_data in pictures_data:
    if isinstance(picture_data, str):
      picture = GunPictures(
          picture_url=picture_data,
          gun=gun
      )
    else:
      picture = GunPictures(
          picture_url=picture_data.get('picture_url'),
          description=picture_data.get('description'),
          gun=gun
      )
      db.session.add(picture)


@guns.route('/', methods=['POST'])
@login_required
def create():
  try:
    gun_body = request.get_json() if request.is_json else request.form
    gun_data = parse_gun_data(gun_body)

    gun_data['seller_id'] = current_user.id

    pictures_data = request.get_json().data.get(
      'pictures', []) if request.is_json else request.form.getlist('pictures')

    required_fields = ['model', 'caliber', 'capacity', 'action', 'price']
    missing_fields = [
      field for field in required_fields if not gun_data.get(field)]
    if missing_fields:
      return api_response.error(
        message="Missing required fields",
        code=400,
        errors=missing_fields
      )

    # * Pake ** buat ubah gun_data dari json jadi parameter di Gun (jadi gak perlu nulis satu persatu)
    gun = Gun(**gun_data)
    db.session.add(gun)

    if pictures_data:
      create_gun_pictures(gun, pictures_data)

    db.session.commit()
    return api_response.success(
      data=gun.to_dict(include_relationships=['seller']),
      message='Gun created successfully',
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


@guns.route('/', methods=['GET'])
def get_guns():
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('page_size', 10, type=int)

  guns_query = Gun.query

  return api_response.paginate(
      query=guns_query,
      page=page,
      page_size=page_size,
      include_relationships=['seller'],
    )


@guns.route('/<int:id>', methods=['GET'])
def get_gun_by_id(id):
  gun = Gun.query.get(id)

  if not gun:
    return api_response.error(
      message='Gun not found',
      code=404,
      errors=gun
    )

  return api_response.success(
    data=gun.to_dict(include_relationships=['seller'])
  )


@guns.route('/<int:id>', methods=['PATCH', 'DELETE'])
@login_required
def update_and_delete_gun_by_id(id):
  gun = Gun.query.get(id)

  if not gun:
    return api_response.error(
      message='Gun not found',
      code=404,
      errors=gun
    )

  if request.method == 'PATCH':
    try:
      gun_body = request.get_json() if request.is_json else request.form
      gun_data = parse_gun_data(gun_body)

      pictures_data = request.get_json().data.get(
        'pictures', []) if request.is_json else request.form.getlist('pictures')

      for key, value in gun_data.items():
        if value is not None:
          setattr(gun, key, value)

      if pictures_data:
        for picture in gun.pictures:
          db.session.delete(picture)

        create_gun_pictures(gun, pictures_data)

      db.session.commit()
      return api_response.success(
        message="Success update gun",
        data=gun.to_dict(include_relationships=['seller']),
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
      for picture in gun.pictures:
        db.session.delete(picture)

      db.session.delete(gun)
      db.session.commit()

      return api_response.success(
        message=f"Successfully delete gun with id:{id}"
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


@guns.route('/create-batch', methods=['POST'])
@login_required
def batch_create():
  try:
    gun_body = request.get_json() if request.is_json else request.form

    if not isinstance(gun_body, list):
      return api_response.error(
        message="Request must be an array of guns",
        code=400
      )

    created_guns = []

    for gun_item in gun_body:
      gun_data = parse_gun_data(gun_item)
      pictures_data = gun_item.get(
        'pictures', []) if request.is_json else request.form.getlist('pictures')

      gun_data['seller_id'] = current_user.id

      gun = Gun(**gun_data)

      if pictures_data:
        create_gun_pictures(gun, pictures_data)

      created_guns.append(gun)

    db.session.bulk_save_objects(created_guns)
    db.session.commit()

    return api_response.success(
      data=[gun.to_dict(include_relationships=['seller'])
            for gun in created_guns],
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


@guns.route('/delete-batch', methods=['DELETE'])
@login_required
def batch_delete():
  try:
    guns = Gun.query.all()

    for gun in guns:
      db.session.delete(gun)  # Hapus satu per satu
    db.session.commit()
    return api_response.success(
      message="All guns deleted successfully"
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
