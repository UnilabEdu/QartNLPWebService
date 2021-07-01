from flask import Blueprint, render_template, request
from app.main.temp_data import people, block_files, grammar_blocks, checkboxes, word_list # TODO: მონაცემების წამოღება ბაზიდან
from app import babel
from app.settings import Config


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.LANGUAGES.keys())


main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates/jinja'
                           )


@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', blocks=grammar_blocks)


@main_blueprint.route('/documentation', methods=['GET', 'POST'])
def documentation():
    return render_template('files.html', block_files=block_files)


@main_blueprint.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('about.html', people=people)


@main_blueprint.route('/add_files', methods=['GET', 'POST'])
def add_files():
    return render_template('add-file.html', checkboxes=checkboxes)


@main_blueprint.route('/concrete', methods=['GET', 'POST'])
def concrete():
    return render_template('concrete.html', word_list=word_list)
