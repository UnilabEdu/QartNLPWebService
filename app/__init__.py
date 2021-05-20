from flask import Flask
from flask_migrate import Migrate

from app.settings import Config
from app.models import db


migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # inserting configurations from settings
    app.config.from_object(Config)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db, render_as_batch=True)

    # Blueprint registrations
    from app.main.views import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    return app
