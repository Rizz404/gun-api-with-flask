from flask import request, Blueprint, jsonify

from gundevilapp.app import db
from gundevilapp.guns.models import Gun, GunPictures

guns = Blueprint('guns', __name__, template_folder='templates')


def parse_gun_data(data, is_form=False):
  # * Helper function buat parse data buat form dan juga json
  if is_form:
    return {
      'model': data.get('model'),
      'caliber': int(data.get('caliber')) if data.get('caliber') else None,
      'capacity': int(data.get('capacity')) if data.get('capacity') else None,
      'length': int(data.get('length')) if data.get('length') else None,
      'weight': int(data.get('weight')) if data.get('weight') else None,
      'action': data.get('action'),
      'price': int(data.get('price')) if data.get('price') else None,
      'description': data.get('description'),
      'stock': int(data.get('stock')) if data.get('stock') else 0
    }
  return {
    'model': data.get('model'),
    'caliber': data.get('caliber'),
    'capacity': data.get('capacity'),
    'length': data.get('length'),
    'weight': data.get('weight'),
    'action': data.get('action'),
    'price': data.get('price'),
    'description': data.get('description'),
    'stock': data.get('stock', 0)
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


@guns.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    guns = Gun.query.all()
    guns_list = [gun.to_dict() for gun in guns]

    return jsonify(guns_list)

  elif request.method == 'POST':
    try:
      if request.is_json:
        data = request.get_json()
        gun_data = parse_gun_data(data)
        pictures_data = data.get('pictures', [])
      else:
        gun_data = parse_gun_data(request.form, is_form=True)
        pictures_data = request.form.getlist('pictures')

      required_fields = ['model', 'caliber', 'capacity', 'action', 'price']
      missing_fields = [
        field for field in required_fields if not gun_data.get(field)]
      if missing_fields:
        return jsonify({
          'error': f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

      gun = Gun(**gun_data)
      db.session.add(gun)

      if pictures_data:
        create_gun_pictures(gun, pictures_data)

      db.session.commit()
      return jsonify(gun.to_dict()), 201
    except ValueError as e:
      db.session.rollback()
      return jsonify({'error': str(e)}), 400
    except Exception as e:
      return jsonify(str(e)), 500


@guns.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def with_id(id):
  gun = Gun.query.get(id)

  if not gun:
    return jsonify({"error": "Gun not found"}), 404

  if request.method == 'GET':
    return jsonify(gun.to_dict())

  elif request.method == 'PATCH':
    try:
      if request.is_json:
        data = request.get_json()
        gun_data = parse_gun_data(data)
        pictures_data = data.get('pictures', [])
      else:
        gun_data = parse_gun_data(request.form, is_form=True)
        pictures_data = request.form.getlist('pictures')

      for key, value in gun_data.items():
        if value is not None:
          setattr(gun, key, value)

      if pictures_data:
        for picture in gun.pictures:
          db.session.delete(picture)

        create_gun_pictures(gun, pictures_data)

      db.session.commit()
      return jsonify(gun.to_dict())
    except ValueError as e:
      db.session.rollback()
      return jsonify({'error': str(e)}), 400
    except Exception as e:
      return jsonify(str(e)), 500

  elif request.method == 'DELETE':
    try:
      for picture in gun.pictures:
        db.session.delete(picture)

      db.session.delete(gun)
      db.session.commit()

      return jsonify({
        'message': f'Gun with id {id} successfully deleted'
      })
    except ValueError as e:
      db.session.rollback()
      return jsonify({'error': str(e)}), 400
    except Exception as e:
      return jsonify(str(e)), 500


@guns.route('/create-batch', methods=['POST'])
def batch_create():
  try:
    if not request.is_json:
      return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()

    if not isinstance(data, list):
      return jsonify({'error': 'Request must be an array of guns'}), 400

    created_guns = []

    for gun_item in data:
      gun_data = parse_gun_data(gun_item)
      pictures_data = gun_item.get('pictures', [])

      gun = Gun(**gun_data)

      db.session.add(gun)

      if pictures_data:
        create_gun_pictures(gun, pictures_data)

      created_guns.append(gun)

    db.session.commit()
    return jsonify([gun.to_dict() for gun in created_guns]), 201
  except ValueError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 500


@guns.route('/delete-batch', methods=['DELETE'])
def batch_delete():
  try:
    guns = Gun.query.all()

    for gun in guns:
      db.session.delete(gun)  # Hapus satu per satu
    db.session.commit()
    return jsonify({'message': 'All guns deleted successfully'})
  except ValueError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 500
