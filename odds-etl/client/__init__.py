import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


BASE_URL = 'http://localhost:5002/v1'


class OddsApiClient:
    def __init__(self):
        self._session = self._build_session()
        self._base_url = BASE_URL

    @staticmethod
    def _build_session():
        status_forcelist = frozenset([500, 502, 503, 504])
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.3,
            status_forcelist=status_forcelist
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        return session

    def _get(self, url, params):
        return self._session.get(url, params=params)

    def _post(self, url, data):
        return self._session.post(url, json=data)

    def _put(self, url, data):
        return self._session.put(url, json=data)

    def get_odds(self, params=None):
        return self._get(f'{BASE_URL}/odds', params)

    def add_odds(self, data):
        return self._get(f'{BASE_URL}/odds', data)

    def get_odds_filters(self, odds_uuid, params=None):
        return self._get(f'{BASE_URL}/{odds_uuid}/filters', params)

    def add_odds_filters(self, odds_uuid, data):
        return self._get(f'{BASE_URL}/{odds_uuid}/filters', data)

    def get_game(self, game_id):
        return self._get(f'{BASE_URL}/games/{game_id}', None)

    def add_games(self, data):
        return self._post(f'{BASE_URL}/games', data)

