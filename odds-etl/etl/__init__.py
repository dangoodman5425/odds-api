from etl.entity import PlayerProp, PregameOdd
from sportsdata import SportsDataClient
from client import OddsApiClient
import datetime
import requests


odds_api = 'http://localhost:5002/v1/odds'
client = OddsApiClient()


# datetime.datetime.strptime(odds['DateTime'], '%Y-%m-%dT%H:%M:%S').strftime('%m-%d-%y %I:%M%p')


def get_props(sport, date):
    player_props = client.player_odds_by_date(sport, date)
    for odds in player_props:
        if odds['Description'] == 'Fantasy Points':
            continue
        game = client.get_game(odds['GameId'])
        PlayerProp(player_name=odds['Name'], team=odds['Team'], game=game, stat=odds['Description'],
                   line=odds['OverUnder'], sport=sport).upload()


def get_pregame_odds(sport, date):
    pregame_odds_data = client.pregame_odds_by_date(sport, date)
    for game in pregame_odds_data:
        PregameOdd().upload()


def get_games(sport, date):
    games_data = client.pregame_odds_by_date(sport, date)
    client.add_games([{'game_id': game['GameID'],
                       'home_team_id': game['HomeTeamID'], 'away_team_id': game['AwayTeamID'],
                       'home_team_nickname': game['HomeTeam'], 'away_team_nickname': game['AwayTeam'],
                       'game_time': game['DateTime']} for game in games_data])


def main(date=datetime.datetime.today().strftime('%Y-%m-%d'), sport='nba'):
    pregame_odds_data = client.pregame_odds_by_date(sport, date)
    for game in pregame_odds_data:
        game_time = datetime.datetime.strptime(game['DateTime'], '%Y-%m-%dT%H:%M:%S').strftime('%m-%d-%y %I:%M%p')
        home_team = game['HomeTeamName']
        away_team = game['AwayTeamName']
        odds_data = game['PregameOdds'][0]
        over_under = odds_data['OverUnder']
        home_spread = odds_data['HomePointSpread']
        payload = {'odds_name': f'{away_team} @ {home_team} O{over_under}', 'odds_type': 'Over/Under',
                   'snippet': game_time}
        res = requests.post(odds_api, json=payload)
        odds_uuid = res.json()['data']['odds_uuid']
        requests.post(f'{odds_api}/{odds_uuid}/filters', json=[{'filter_type': 'sport', 'filter_name': sport},
                                                               {'filter_type': 'bet_type', 'filter_name': 'ou'},
                                                               {'filter_type': 'team', 'filter_name': home_team},
                                                               {'filter_type': 'odd_type', 'filter_name': 'game'}])
        home_spread = f'+{home_spread}' if home_spread > 0 else home_spread
        payload = {'odds_name': f'{home_team} {home_spread}', 'odds_type': 'Spread',
                   'snippet': f'{away_team} @ {home_team} {game_time}'}
        res = requests.post(odds_api, json=payload)
        odds_uuid = res.json()['data']['odds_uuid']
        requests.post(f'{odds_api}/{odds_uuid}/filters', json=[{'filter_type': 'sport', 'filter_name': sport},
                                                               {'filter_type': 'bet_type', 'filter_name': 'spread'},
                                                               {'filter_type': 'team', 'filter_name': home_team},
                                                               {'filter_type': 'odd_type', 'filter_name': 'game'}])
        get_props(sport, date)


def clean():
    pass


def upload():
    pass


if __name__ == '__main__':
    client = SportsDataClient()
    main(date="2020-01-01")
