from flask import Flask
from flask_migrate import Migrate
from flask_user import SQLAlchemyAdapter, UserManager
from flask_mail import Mail


from celery import Celery

from app.settings import Config
from app.models import db

from app.user.user_model import User, Role, UserRoles
from app.user.admin.admin import admin

migrate = Migrate()
mail = Mail()


# db_adapter = SQLAlchemyAdapter(db, User)
# user_manager = UserManager(db_adapter)
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)


def create_app():
    app = Flask(__name__)

    # inserting configurations from settings
    app.config.from_object(Config)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db, render_as_batch=True)

    #Init Celery
    celery.conf.update(app.config)

    # Setup Flask-Mail
    mail.init_app(app)

    # Setup Flask-User

    # user_manager.init_app(db_adapter, app)
    db_adapter = SQLAlchemyAdapter(db, User)
    UserManager(db_adapter, app)

    # user_manager.init_app(app)

    # db_adapter = SQLAlchemyAdapter(db, User)
    # user_manager.init_app(app, db_adapter)
    # user_manager.init_app(db_adapter)

    # Setup Flask-Admin
    admin.init_app(app)

    # Blueprint registrations
    from app.main.views import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    from app.file_processing.views import file_processor_blueprint
    app.register_blueprint(file_processor_blueprint, url_prefix="/main")

    return app


# from flask import Flask
# from flask_migrate import Migrate
#
# from app.settings import Config
# from app.models import db
#
#
# migrate = Migrate()


# def create_app():
#     app = Flask(__name__)
#
#     # inserting configurations from settings
#     app.config.from_object(Config)
#
#     # Setup Flask-SQLAlchemy
#     db.init_app(app)
#
#     # Setup Flask-Migrate
#     migrate.init_app(app, db, render_as_batch=True)
#
#     # Blueprint registrations
#     from app.main.views import main_blueprint
#     app.register_blueprint(main_blueprint, url_prefix="/")
#
#     return app
