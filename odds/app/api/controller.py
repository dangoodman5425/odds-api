from flask import request
from flask_restplus import Resource
from webargs import fields
from webargs.flaskparser import use_args

from app.api.model import Odds, OddsFilter
from app.api.service import get_odds_by, get_odds_filter_by
from app.api.support import json_response, create_entity, update_entity, create_entities
from app.api.validation import CreateOddsSchema, UpdateOddsSchema, CreateOddsFilterSchema


class OddsPing(Resource):

    @staticmethod
    @json_response
    def get():
        return {'status': 'success', 'message': 'pong'}, 200


class OddsList(Resource):

    odds_args = {
        'odds_name': fields.String(),
        'odds_type': fields.String(),
        'sport': fields.String(),
        'per_page': fields.Integer(),
        'page': fields.Integer(),
        'filter_type': fields.String(),
        'filter_name': fields.String(),
        'active': fields.Boolean(),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_response = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }

        self._create_odds_schema = CreateOddsSchema()

    @use_args(odds_args)
    @json_response
    def get(self, query_params):
        return get_odds_by(**query_params), 200

    @json_response
    def post(self):
        req = request.get_json()
        errors = self._create_odds_schema.validate(req)
        if errors:
            return self._default_response, 422
        return create_entity(Odds(**req))


class OddsDetails(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_response = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }

        self._update_odds_schema = UpdateOddsSchema()

    @staticmethod
    @json_response
    def get(odds_uuid):
        """Gets a listing for a given odds UUID (this should be made less janky in the future)

        :param odds_uuid: Odds UUID corresponding to the listing
        :return: JSON response containing the listing, and a status code
        """
        return get_odds_by(odds_uuid=odds_uuid)['data'][0], 200

    @json_response
    def put(self, odds_uuid):
        req = request.get_json()
        errors = self._update_odds_schema.validate(req)
        if errors:
            return self._default_response, 422
        return update_entity(Odds, {'odds_uuid': odds_uuid}, **req), 200


class OddsFilterDetails(Resource):

    odds_filter_args = {
        'filter_type': fields.String(),
        'filter_name': fields.String(),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_response = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }

        self._create_odds_filter_schema = CreateOddsFilterSchema()

    @staticmethod
    @json_response
    def get(odds_uuid):
        return get_odds_filter_by(odds_uuid), 200

    @json_response
    def post(self, odds_uuid):
        return create_entities([OddsFilter(odds_uuid=odds_uuid, **req) for req in request.get_json()])