from app import db
from app.api.model import Odds, OddsFilter, Game


def get_odds():
    """Retrieves all entries from the `odds` table
    :return: List of dictionary representation of each entry
    """
    return {'data': [x.to_dict() for x in Odds.query.all()]}


def get_odds_by_uuid(odds_uuid):
    """Retrieves entry from the `odds` table based on odds_uuid
    :return: Dictionary representation of each entry
    """
    return [x.to_dict() for x in Odds.query.filter_by(odds_uuid=odds_uuid).all()][0]


def get_odds_by(**kwargs):
    """Retrieves entries from the `odds` table based on conditions
    :return: List of dictionary representation of each entry
    """
    page = kwargs.pop('page', 1)
    per_page = kwargs.pop('per_page', 250)
    filter_name = kwargs.pop('filter_name', None)
    query = db.session.query(Odds)\
        .filter_by(**kwargs)
    if filter_name:
        query = query.outerjoin(OddsFilter).filter_by(filter_name=filter_name)
    paginate = query.paginate(page=page, per_page=per_page)
    return {'data': [odds.to_dict() for odds in paginate.items], 'has_next': paginate.has_next}


def get_odds_filter_by(odds_uuid):
    """Retrieves entries from the `odds_filter` table based on odds_uuid
    :return: List of dictionary representation of each entry
    """
    return {'data': [x.to_dict() for x in OddsFilter.query.filter_by(odds_uuid=odds_uuid).all()]}


def get_games_by(**kwargs):
    """Retrieves entries from the `game` table based on filters
    :return: List of dictionary representation of each entry
    """
    return {'data': [x.to_dict() for x in Game.query.filter_by(**kwargs).all()]}
