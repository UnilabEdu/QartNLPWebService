from flask import Blueprint, render_template
<<<<<<< HEAD

=======
from app.main.temp_data import people, block_files # TODO: მონაცემების წამოღება ბაზიდან
>>>>>>> 04e6ff5babe873b72282b9473c4db6793d545be1
main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates'
                           )


@main_blueprint.route('/', methods=['GET', 'POST'])
<<<<<<< HEAD
def home():
    pass
=======
@main_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
>>>>>>> 04e6ff5babe873b72282b9473c4db6793d545be1


@main_blueprint.route('/documentation', methods=['GET', 'POST'])
def documentation():
<<<<<<< HEAD
    pass
=======
    return render_template('files.html', block_files=block_files)
>>>>>>> 04e6ff5babe873b72282b9473c4db6793d545be1


@main_blueprint.route('/about_us', methods=['GET', 'POST'])
def about_us():
<<<<<<< HEAD
    pass
=======
    return render_template('about.html', people=people)


>>>>>>> 04e6ff5babe873b72282b9473c4db6793d545be1

