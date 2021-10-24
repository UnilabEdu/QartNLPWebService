from flask import Blueprint, render_template, request
from flask_login import login_user

from app.extentions import babel
from app.main.temp_data import people, block_files, grammar_blocks
from app.settings import Config
from app.user.user_model import User

main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates/jinja',
                           url_prefix='/'
                           )


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.LANGUAGES.keys())


@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    login_user(User.query.get(1))
    return render_template('main.html', blocks=grammar_blocks)


@main_blueprint.route('/documentation', methods=['GET', 'POST'])
def documentation():
    return render_template('files.html', block_files=block_files)


@main_blueprint.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('about.html', people=people)
