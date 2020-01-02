from flask import Blueprint
from flask_restplus import Api

from app.api.controller import OddsPing, OddsList, OddsDetails, OddsFilterDetails

VERSION = 'v1'

odds_blueprint = Blueprint('odds', __name__)
api = Api(odds_blueprint)


api.add_resource(OddsPing, f'/{VERSION}/odds/ping')
api.add_resource(OddsList, f'/{VERSION}/odds')
api.add_resource(OddsDetails, f'/{VERSION}/odds/<odds_uuid>')
api.add_resource(OddsFilterDetails, f'/{VERSION}/odds/<odds_uuid>/filters')
