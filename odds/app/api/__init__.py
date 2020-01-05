from flask import Blueprint
from flask_restplus import Api

from app.api.controller import OddsPing, OddsList, OddsDetails, OddsFilterDetails, Games, GameDetails

VERSION = 'v1'

odds_blueprint = Blueprint('odds', __name__)
api = Api(odds_blueprint)


api.add_resource(OddsPing, f'/{VERSION}/odds/ping')
api.add_resource(OddsList, f'/{VERSION}/odds')
api.add_resource(OddsDetails, f'/{VERSION}/odds/<odds_uuid>')
api.add_resource(OddsFilterDetails, f'/{VERSION}/odds/<odds_uuid>/filters')

api.add_resource(Games, f'/{VERSION}/games')
api.add_resource(GameDetails, f'/{VERSION}/games/<game_id>')
