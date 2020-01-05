from datetime import datetime

from client import OddsApiClient

BASE_ODDS_ENDPOINT = 'http://localhost:5002/v1/odds'


IMAGES = {1: 'b82af08a-f700-46c8-aca6-df0d658974bf', 2: 'e5e0d7e4-ae4f-4e29-93f9-35a3d55d4e7b', 3: '6029a338-5ed4-4400-adc2-76ead692abf8', 4: 'cc246af3-1945-42b5-a77b-d00310f2188f', 5: '32c2491a-8939-4aea-98b1-c2ee2a028575', 6: 'dd472676-1398-4b3f-b2ed-96b7c6f797d5', 7: 'c0e62330-f10d-466c-9988-d545875de160', 8: 'e81518af-ad44-4b64-af88-b29572de08bc', 9: 'a4ee974d-3d6f-42fc-a470-1357c0fdb565', 10: '7d174e41-3eeb-4773-a298-f717bdeccf14', 11: '5200e3f5-39f9-4952-ac43-edb59d67ba94', 12: 'e4a38b5e-7204-48e8-a36c-85eb0c589d79', 13: 'e01b5a13-8155-4f1f-b3d0-0ed8a1ed1c1d', 14: '32b28893-940f-4d11-8734-44cc4cac055d', 15: '941b086c-6466-4777-93e4-279ead258452', 16: '2c5b0313-d71f-4d13-8f2f-a1d167e7d60a', 17: 'c2798439-ac72-431a-a17e-9b56380a2264', 18: 'f4db8c3c-cef2-433c-bf01-f5fb14cd129b', 19: '78736572-35bd-4213-b817-3197b5fd5be4', 20: 'facf60f4-965d-4341-a987-448027121461', 21: '2b61f564-58d2-4053-86f8-2aa6047623fd', 22: '69a8353d-d02d-479b-a664-e9e3e8028642', 23: '0778bd90-5da4-48d5-a340-e473f76989d0', 24: '98af56e4-3573-4583-8022-fcb68602d60b', 25: '07a39a5e-a7c1-4f5f-8294-7fcccc71380d', 26: 'c874bccb-b4ec-484d-b580-7466a1e8a868', 27: 'c0a190dd-8135-465e-ac44-efb932c666c9', 28: '95ca6493-f387-4da0-8e99-0d7b5164dd17', 29: 'efde7d18-06e2-4909-933f-6653b387b5c1', 30: 'f9375459-d702-452d-9758-0c91646ea6d5'}


class BaseOdds:

    def __init__(self, sport, bet_type, team, team_id=None):
        self._sport = sport
        self._bet_type = bet_type
        self._team = team
        self._client = OddsApiClient()
        # Shittie please change later
        self._image_uuid = IMAGES[team_id] if team_id else None

    def odds_name(self):
        pass

    def snippet(self):
        pass

    def _generate_odds_payload(self):
        # Shittie change later
        data = {'odds_name':  self.odds_name(), 'odds_type': self._bet_type, 'snippet': self.snippet()}
        if self._image_uuid:
            data['image_uuid'] = self._image_uuid
        return data

    def _generate_filters_payload(self):
        return [{'filter_type': 'sport', 'filter_name': self._sport},
                {'filter_type': 'bet_type', 'filter_name': self._bet_type},
                {'filter_type': 'team', 'filter_name': self._team},
                {'filter_type': 'odd_type', 'filter_name': 'game'}]

    def upload(self):
        odds_uuid = self._client.add_odds(self._generate_odds_payload()).json()['data']['odds_uuid']
        self._client.add_odds_filters(odds_uuid, self._generate_filters_payload())


class PlayerProp(BaseOdds):

    def __init__(self, player_name, team, game, stat, line, sport):
        super().__init__(sport=sport, bet_type='Player Prop', team=team, team_id=game['home_team_id'])
        self._player_name = player_name
        self._team = team
        # Game dictionary entity (response from Game endpoint) e.g. {'game_id': 12345, 'home_team_id': 17,
        # 'away_team_id': 14, 'game_time': ...}
        self._game = game
        # e.g. Points, Rebounds
        self._stat = stat
        self._line = line

    def odds_name(self):
        # Derrick Rise (DET) O23 Points
        return f'{self._player_name} ({self._team}) O{self._line} {self._stat}'

    def snippet(self):
        # DET @ CHI 7:30PM
        return '{} @ {} {}'.format(self._game['home_team_nickname'], self._game['home_team_nickname'],
                                   get_formatted_gt(self._game['game_time']))


class PregameOdd(BaseOdds):

    def __init__(self, game, bet_type, line, sport):
        super().__init__(sport=sport, bet_type=bet_type, team=game['home_team_nickname'], team_id=game['home_team_id'])
        # Game dictionary entity (response from Game endpoint) e.g. {'game_id': 12345, 'home_team_id': 17,
        # 'away_team_id': 14, 'game_time': ...}
        self._game = game
        self._bet_type = bet_type
        # e.g. Points, Rebounds
        self._line = line
        self._sport = sport

    def odds_name(self):
        if self._bet_type == 'Spread':
            spread = f'+{self._line}' if self._line > 0 else self._line
            return '{home_team} {spread}'.format(home_team=self._game['home_team_nickname'], spread=spread)
        elif self._bet_type == 'Over/Under':
            return '{away_team} @ {home_team} O{line}'.format(away_team=self._game['away_team_nickname'],
                                                              home_team=self._game['home_team_nickname'],
                                                              line=self._line)
        return ''

    def snippet(self):
        # DET @ CHI 7:30PM
        return '{away_team} @ {home_team} {game_time}'.format(away_team=self._game['away_team_nickname'],
                                                              home_team=self._game['home_team_nickname'],
                                                              game_time=get_formatted_gt(self._game['game_time']))


def get_formatted_gt(game_time):
    return datetime.strptime(game_time, '%a, %d %b %Y %H:%M:%S GMT').strftime('%m-%d-%y %I:%M%p')
