from flask.cli import FlaskGroup
import csv
import uuid

from app import create_app, db
from app.api.model import Odds, OddsFilter

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    """Drops all tables and recreates them in the database
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    """Seeds the database
    """
    with open('/home/dan/Projects/github.com/otb/odds-api/odds/static/odds.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            db.session.add(Odds(odds_uuid=uuid.UUID(line[0]), odds_name=line[1], odds_type=line[2], snippet=line[3],
                                image_uuid=uuid.UUID(line[4])))
    with open('/home/dan/Projects/github.com/otb/odds-api/odds/static/odds_filter.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            db.session.add(OddsFilter(odds_uuid=line[0], filter_type=line[1], filter_name=line[2]))

    db.session.commit()


# app.run(port=5002)


if __name__ == '__main__':
    cli()
