from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
cache = Cache()


def create_app():
    """Registers all blueprints and initializes all application features - including database
    :return: Flask application with all configurations
    """
    app = Flask(__name__)

    app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)
    # Allows for cross-origin support
    cors.init_app(app)
    # Initializes cache
    cache.init_app(app)

    # Register API blueprints
    from app.api import odds_blueprint
    app.register_blueprint(odds_blueprint)

    return app


db = SQLAlchemy()
