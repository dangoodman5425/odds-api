from sportsdata import SportsDataClient
import datetime
import requests


odds_api = 'http://localhost:5002/v1/odds'


def main(date=datetime.datetime.today().strftime('%Y-%m-%d'), sport='nba'):
    pregame_odds_data = client.pregame_odds_by_date(sport, date)
    for i, game in enumerate(pregame_odds_data):
        print(i)
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
    player_odds = client.player_odds_by_date(sport, date)
    for i, odds in enumerate(player_odds):
        print(i)
        if odds['Description'] == 'Fantasy Points':
            continue
        game_time = datetime.datetime.strptime(odds['DateTime'], '%Y-%m-%dT%H:%M:%S').strftime('%m-%d-%y %I:%M%p')
        player_name = odds['Name']
        team = odds['Team']
        over_under = odds['OverUnder']
        stat = odds['Description']
        payload = {'odds_name': f'{player_name} ({team}) O{over_under} {stat}', 'odds_type': 'Player Prop',
                   'snippet': f'{game_time}'}
        res = requests.post(odds_api, json=payload)
        odds_uuid = res.json()['data']['odds_uuid']
        requests.post(f'{odds_api}/{odds_uuid}/filters', json=[{'filter_type': 'sport', 'filter_name': sport},
                                                               {'filter_type': 'bet_type', 'filter_name': 'prop'},
                                                               {'filter_type': 'team', 'filter_name': team},
                                                               {'filter_type': 'odd_type', 'filter_name': 'game'}])


def clean():
    pass


def upload():
    pass


if __name__ == '__main__':
    client = SportsDataClient()
    main(date="2020-01-01")
