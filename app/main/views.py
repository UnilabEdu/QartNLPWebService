from flask import Blueprint, render_template

main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates'
                           )


@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    pass


@main_blueprint.route('/documentation', methods=['GET', 'POST'])
def documentation():
    pass


@main_blueprint.route('/about_us', methods=['GET', 'POST'])
def about_us():
    pass

