from app import db
from app.api.model import Odds, OddsFilter


def get_odds():
    """Retrieves all entries from the `odds` table
    :return: List of dictionary representation of each entry
    """
    return {'data': [x.to_dict() for x in Odds.query.all()]}


def get_odds_by(**kwargs):
    """Retrieves entries from the `odds` table based on conditions
    :return: List of dictionary representation of each entry
    """
    page = kwargs.pop('page', 1)
    per_page = kwargs.pop('per_page', 250)
    paginate = db.session.query(Odds)\
        .outerjoin(OddsFilter)\
        .filter_by(**kwargs)\
        .paginate(page=page, per_page=per_page)
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
    return {'data': [x.to_dict() for x in OddsFilter.query.filter_by(**kwargs).all()]}
