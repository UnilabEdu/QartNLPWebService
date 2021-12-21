from celery import Celery
from flask_babel import Babel
from flask_babel import gettext as _
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session

from app.settings import Config

migrate = Migrate()
mail = Mail()
babel = Babel()
session = Session()
login_manager = LoginManager()
login_manager.login_view = 'main.home'
login_manager.login_message = _('გთხოვთ გაიაროთ ავტორიზაცია')
login_manager.login_message_category = 'danger'
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
