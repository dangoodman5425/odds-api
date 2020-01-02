import datetime
import uuid

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from sqlalchemy.dialects.postgresql import UUID


class Odds(db.Model):
    __tablename__ = 'odds'
    odds_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    odds_uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    odds_name = db.Column(db.String(128), nullable=False)
    odds_type = db.Column(db.String(128), nullable=False)
    snippet = db.Column(db.String(128), nullable=False)
    image_uuid = db.Column(UUID(as_uuid=True))
    active = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, odds_name, odds_type, snippet, active=True, image_uuid=None, odds_uuid=None):
        self.odds_name = odds_name
        self.odds_type = odds_type
        self.snippet = snippet

        self.active = active
        self.image_uuid = image_uuid
        self.odds_uuid = uuid.uuid4() if not odds_uuid else odds_uuid

    def to_dict(self):
        return {
            'odds_name': self.odds_name,
            'odds_uuid': self.odds_uuid,
            'image_uuid': self.image_uuid,
            'snippet': self.snippet,
            'odds_type': self.odds_type,
        }


class OddsFilter(db.Model):
    ___tablename__ = 'odds_filter'
    odds_filter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    odds_uuid = db.Column(UUID(as_uuid=True), ForeignKey('odds.odds_uuid'), nullable=False)
    odds_parent = relationship('Odds')

    filter_type = db.Column(db.String(128), nullable=False)
    filter_name = db.Column(db.String(128), nullable=False)

    def __init__(self, odds_uuid, filter_type, filter_name):
        self.odds_uuid = odds_uuid
        self.filter_type = filter_type
        self.filter_name = filter_name

    def to_dict(self):
        return {
            'odds_uuid': self.odds_uuid,
            'filter_type': self.filter_type,
            'filter_name': self.filter_name,
        }


class Game(db.Model):
    ___tablename__ = 'game'
    game_id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, nullable=False)
    away_team_id = db.Column(db.Integer, nullable=False)
    home_team_nickname = db.Column(db.String(128), nullable=False)
    away_team_nickname = db.Column(db.String(128), nullable=False)
    game_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, game_id, home_team_id, away_team_id, home_team_nickname, away_team_nickname, game_time):
        self.game_id = game_id
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.home_team_nickname = home_team_nickname
        self.away_team_nickname = away_team_nickname
        self.game_time = datetime.datetime.strptime(game_time, '%Y-%m-%dT%H:%M:%S')

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'home_team_id': self.home_team_id,
            'away_team_id': self.away_team_id,
            'home_team_nickname': self.home_team_nickname,
            'away_team_nickname': self.away_team_nickname,
            'game_time': self.game_time,
        }
