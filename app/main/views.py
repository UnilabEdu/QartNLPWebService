from flask import Blueprint, render_template
from app.main.temp_data import people, block_files  # TODO: მონაცემების წამოღება ბაზიდან
main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates'
                           )


@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@main_blueprint.route('/documentation', methods=['GET', 'POST'])
def documentation():
    return render_template('files.html', block_files=block_files)


@main_blueprint.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('about.html', people=people)
