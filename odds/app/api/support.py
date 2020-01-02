from flask import make_response, jsonify
from sqlalchemy.exc import IntegrityError

from app import db


def create_entity(entity):
    """Creates an entry in table in the database
    :return: JSON containing whether household entity has been successful (if not then an error), the created entity,
    and the status code
    """
    try:
        db.session.add(entity)
        db.session.commit()
        return {'result': 'success', 'data': entity.to_dict()}, 202
    except IntegrityError as e:
        return {'result': 'failure', 'reason': 'duplicate entries', 'error': str(e)}, 422
    except Exception as e:
        print(e)
        return {'result': 'failure', 'reason': 'unknown', 'error': str(e)}, 500


def create_entities(entities):
    try:
        db.session.bulk_save_objects(entities)
        db.session.commit()
        return {'result': 'success'}, 202
    except IntegrityError as e:
        return {'result': 'failure', 'reason': 'duplicate entries', 'error': str(e)}, 422
    except Exception as e:
        print(e)
        return {'result': 'failure', 'reason': 'unknown', 'error': str(e)}, 500


def update_entity(table, entity_id, **kwargs):
    """Updates an entry in `TABLE` corresponding with the given household_id
    :param table: table object to update
    :param entity_id: dictionary containing identifier name and value for the entry that will be updated
    :param kwargs: mappings of columns to value which will be updated
    :return: JSON containing whether household entity has been successful (if not then an error) and the status code
    """
    try:
        db.session.query(table).filter_by(**entity_id).update(kwargs)
        db.session.commit()
        return jsonify({'result': 'success'}), 200
    except Exception as e:
        return jsonify({'result': 'failure', 'reason': 'unknown', 'error': str(e)}), 500


def json_response(func):
    def wraps(*args, **kwargs):
        blob, status_code = func(*args, **kwargs)
        return make_response(jsonify(blob), status_code)
    return wraps
