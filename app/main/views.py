from flask import Blueprint, render_template, request
from flask_login import login_user, logout_user

from app.extensions import babel
from app.main.temp_data import people, block_files, grammar_blocks
from app.settings import Config
from app.models.user import User

main_blueprint = Blueprint('main',
                           __name__,
                           url_prefix='/'
                           )


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.LANGUAGES.keys())


@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('main/main.html', blocks=grammar_blocks)


@main_blueprint.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('main/about.html', people=people)
