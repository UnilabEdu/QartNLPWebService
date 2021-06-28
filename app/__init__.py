from flask import Flask
from flask_migrate import Migrate
from flask_user import SQLAlchemyAdapter, UserManager
from flask_mail import Mail
from flask_babel import Babel
from celery import Celery

from app.settings import Config
from app.database import db

from app.user.user_model import User, Role, UserRoles
from app.user.admin.admin import admin
from app.api import api

migrate = Migrate()
mail = Mail()
babel = Babel()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)


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

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)
    UserManager(db_adapter, app)

    # Setup Flask-Admin
    admin.init_app(app)

    # Initialize API
    api.init_app(app)

    # Blueprint registrations
    from app.main.views import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    from app.file_processing.views import file_processor_blueprint
    app.register_blueprint(file_processor_blueprint, url_prefix="/")

    return app
