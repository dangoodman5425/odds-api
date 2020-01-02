from client import OddsApiClient

BASE_ODDS_ENDPOINT = 'http://localhost:5002/v1/odds'


class BaseOdds:

    def __init__(self, sport, bet_type, team):
        self._sport = sport
        self._bet_type = bet_type
        self._team = team
        self._client = OddsApiClient()

    def odds_name(self):
        pass

    def snippet(self):
        pass

    def _generate_odds_payload(self):
        return {'odds_name':  self.odds_name(), 'odds_type': 'Player Prop', 'snippet': self.snippet()}

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
        super().__init__(sport=sport, bet_type='prop', team=team)
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
                                   self._game['game_time'])


class PregameOdd(BaseOdds):

    def __init__(self, team, game, stat, line, sport, bet_type):
        super().__init__(sport=sport, bet_type=bet_type, team=team)
        self._team = team
        # Game dictionary entity (response from Game endpoint) e.g. {'game_id': 12345, 'home_team_id': 17,
        # 'away_team_id': 14, 'game_time': ...}
        self._game = game
        self._bet_type = bet_type
        # e.g. Points, Rebounds
        self._stat = stat
        self._line = line
        self._sport = sport

    def odds_name(self):
        if self._bet_type == 'spread':
            spread = f'+{self._line}' if self._line > 0 else self._line
            return '{home_team} {spread}'.format(home_team=self._game['home_team_nickname'], spread=spread)
        elif self._bet_type == 'ou':
            '{away_team} @ {home_team} O{line}'.format(away_team=self._game['away_team_nickname'],
                                                       home_team=self._game['home_team_nickname'],
                                                       line=self._line)
        return ''

    def snippet(self):
        # DET @ CHI 7:30PM
        return '{away_team} @ {home_team} {game_time}'.format(away_team=self._game['away_team_nickname'],
                                                              home_team=self._game['home_team_nickname'],
                                                              game_time=self._game['game_time'])
