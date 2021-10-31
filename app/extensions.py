from celery import Celery
from flask_babel import Babel
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

from app.settings import Config

migrate = Migrate()
mail = Mail()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'გთხოვთ გაიაროთ ავტორიზაცია'
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
