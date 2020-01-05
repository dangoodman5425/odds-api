import requests

from requests.adapters import HTTPAdapter
from urllib3 import Retry

BASE_URL = 'https://api.sportsdata.io'
API_KEY = '1121ae7cdf09443bb29a35ef3d1e80fa'


class SportsDataClient:

    def __init__(self, version='v3', content_type='json'):
        self._base_url = BASE_URL
        self._version = version
        self._content_type = content_type
        self._session = self.build_session()
        self._api_key = API_KEY

    @staticmethod
    def build_session():
        status_forcelist = frozenset([500, 502, 503, 504])
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.3,
            status_forcelist=status_forcelist
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('https://', adapter)
        return session

    def _make_request(self, url):
        return self._session.get(url, params={'key': self._api_key}).json()

    def pregame_odds_by_date(self, sport, date):
        """ Returns a JSON of pregame odds for a given date and sport

        :param sport: sport e.g. nba, nfl, nhl
        :param date: in YYYY-MM-DD format
        :return: JSON of pregame odds
        """
        endpoint = 'GameOddsByDate'
        return self._make_request(
            f'{self._base_url}/{self._version}/{sport}/odds/{self._content_type}/{endpoint}/{date}')

    def player_odds_by_date(self, sport, date):
        """ Returns a JSON of a player prop odds for a given date and sport

        :param sport: sport e.g. nba, nfl, nhl
        :param date: in YYYY-MM-DD format
        :return: JSON of pregame odds
        """
        endpoint = 'PlayerPropsByDate'
        return self._make_request(
            f'{self._base_url}/{self._version}/{sport}/odds/{self._content_type}/{endpoint}/{date}')

    def games_by_date(self, sport, date):
        """ Returns a JSON of all games for a given date and sport

        :param sport: sport e.g. nba, nfl, nhl
        :param date: in YYYY-MM-DD format
        :return: JSON of pregame odds
        """
        endpoint = 'GamesByDate'
        return self._make_request(
            f'{self._base_url}/{self._version}/{sport}/scores/{self._content_type}/{endpoint}/{date}')
