from celery import Celery
from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

from app.api import api
from app.database import db
from app.models.file import File, Statistics, Pages, Sentences, Words
from app.settings import Config
from app.user.admin.admin import admin
from app.user.user_model import User, Role, UserRoles, Profile
from app.commands import reset_db_command, populate_db_command, clear_file_tables_command

migrate = Migrate()
mail = Mail()
babel = Babel()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

COMMANDS = [
    reset_db_command,
    populate_db_command,
    clear_file_tables_command
]


def create_app():
    app = Flask(__name__)

    # inserting configurations from settings
    app.config.from_object(Config)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db, render_as_batch=True)

    # Init Celery
    celery.conf.update(app.config)

    # Setup Flask-Mail
    mail.init_app(app)

    # Setup Flask-Babel
    babel.init_app(app)

    # Setup Flask-Admin
    admin.init_app(app)

    # Initialize API
    api.init_app(app)

    # Flask-Login
    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(id_):
        return User.query.get(id_)

    login_manager.init_app(app)

    # Initialize commands
    initialize_commands(app, COMMANDS)

    # Blueprint registrations
    from app.main.views import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    from app.files.views import file_views_blueprint
    app.register_blueprint(file_views_blueprint, url_prefix="/")

    from app.tagging.views import tagging_blueprint
    app.register_blueprint(tagging_blueprint, url_prefix="/tagging")

    return app


def initialize_commands(app, all_commands):
    for command in all_commands:
        app.cli.add_command(command)
