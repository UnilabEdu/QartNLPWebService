from flask import Flask

from app.api import api
from app.commands import reset_db_command, populate_db_command, clear_file_tables_command
from app.database import db
from app.extentions import migrate, mail, babel, celery, login_manager
from app.settings import Config
from app.user.admin.admin import admin
from app.user.user_model import User

from app.files.views import file_views_blueprint
from app.main.views import main_blueprint
from app.tagging.views import tagging_blueprint


BLUEPRINTS = [
    main_blueprint,
    tagging_blueprint,
    file_views_blueprint
]

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
    # Initialize Celery
    celery.conf.update(app.config)
    # Setup Flask-Mail
    mail.init_app(app)
    # Setup Flask-Babel
    babel.init_app(app)
    # Setup Flask-Admin
    admin.init_app(app)
    # Initialize Flask-RESTful
    api.init_app(app)

    # Flask-Login
    @login_manager.user_loader
    def load_user(id_):
        return User.query.get(id_)

    login_manager.init_app(app)

    # Initialize commands and blueprints
    initialize_commands(app, COMMANDS)
    configure_blueprints(app, BLUEPRINTS)

    return app


def configure_blueprints(app, all_blueprints):
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)


def initialize_commands(app, all_commands):
    for command in all_commands:
        app.cli.add_command(command)
