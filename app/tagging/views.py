from . import tagging_blueprint
from flask import render_template

from .forms import NerTagForm


@tagging_blueprint.route('/test', methods=['GET', 'POST'])
def test():
    form = NerTagForm()
    random_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    tags = [
        {"id": 1, "keys": [5, 6], "value": "ORG"},
        {"id": 2, "keys": [1, 3], "value": "SOMETHING"},
        {"id": 3, "keys": [8, 9], "value": "ELSE"},
        {"id": 4, "keys": [12, 19], "value": "DEV"},
    ]
    return render_template('tagging.html', text=random_text, tags=tags, form=form)
