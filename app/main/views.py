<<<<<<< HEAD
from flask import Blueprint, render_template

main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates'
=======
from flask import Blueprint, render_template, request
from app.main.temp_data import people, block_files  # TODO: მონაცემების წამოღება ბაზიდან
from app.main.temp_data import people, block_files, grammar_blocks, checkboxes, word_list # TODO: მონაცემების წამოღება ბაზიდან
from app import babel
from app.settings import Config


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.LANGUAGES.keys())


main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates/jinja'
>>>>>>> a6a33f9bccc519ec173bcbdcb93395e9f841787f
                           )


@main_blueprint.route('/', methods=['GET', 'POST'])
<<<<<<< HEAD
def home():
    pass
=======
@main_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', blocks=grammar_blocks)
>>>>>>> a6a33f9bccc519ec173bcbdcb93395e9f841787f


@main_blueprint.route('/documentation', methods=['GET', 'POST'])
def documentation():
<<<<<<< HEAD
    pass
=======
    return render_template('files.html', block_files=block_files)
>>>>>>> a6a33f9bccc519ec173bcbdcb93395e9f841787f


@main_blueprint.route('/about_us', methods=['GET', 'POST'])
def about_us():
<<<<<<< HEAD
    pass

=======
    return render_template('about.html', people=people)


@main_blueprint.route('/add_files', methods=['GET', 'POST'])
def add_files():
    return render_template('add-file.html', checkboxes=checkboxes)


@main_blueprint.route('/concrete', methods=['GET', 'POST'])
def concrete():
    return render_template('concrete.html', word_list=word_list)
>>>>>>> a6a33f9bccc519ec173bcbdcb93395e9f841787f
