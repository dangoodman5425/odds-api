import datetime

from client import OddsApiClient
from etl.entity import PlayerProp, PregameOdd
from sportsdata import SportsDataClient

odds_api = 'http://localhost:5002/v1/odds'
client = OddsApiClient()
sports_data_client = SportsDataClient()


def get_props(sport, date):
    player_props = sports_data_client.player_odds_by_date(sport, date)
    for odds in player_props:
        if odds['Description'] == 'Fantasy Points':
            continue
        game = client.get_game(odds['GameID']).json()
        PlayerProp(player_name=odds['Name'], team=odds['Team'], game=game, stat=odds['Description'],
                   line=odds['OverUnder'], sport=sport).upload()


def get_pregame_odds(sport, date):
    pregame_odds_data = sports_data_client.pregame_odds_by_date(sport, date)
    for odds in pregame_odds_data:
        game = client.get_game(odds['GameId']).json()
        pregame_odds = odds['PregameOdds'][0]
        PregameOdd(game, 'Over/Under', pregame_odds['OverUnder'], sport).upload()
        PregameOdd(game, 'Spread', pregame_odds['HomePointSpread'], sport).upload()


def get_games(sport, date):
    games_data = sports_data_client.pregame_odds_by_date(sport, date)
    client.add_games([{'game_id': game['GameId'],
                       'home_team_id': game['HomeTeamId'], 'away_team_id': game['AwayTeamId'],
                       'home_team_nickname': game['HomeTeamName'], 'away_team_nickname': game['AwayTeamName'],
                       'game_time': game['DateTime']} for game in games_data])


def main(date=datetime.datetime.today().strftime('%Y-%m-%d'), sport='nba'):
    get_games(sport, date)
    get_pregame_odds(sport, date)
    get_props(sport, date)


def clean():
    pass


def upload():
    pass


if __name__ == '__main__':
    main(date="2020-01-01")
