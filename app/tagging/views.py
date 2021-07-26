from . import tagging_blueprint
from flask import render_template
import json
from .forms import NerTagForm
from app.models.file import File, Pages


@tagging_blueprint.route('/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
def test(page_id=0, file_id=0):

    file = File.file_by_id(file_id)
    page = file.pages[page_id - 1]

    form = NerTagForm()
    not_random_text_anymore = page.get_text()

    # retrieve page by file_id and page_id
    # retrieve all the tags from the page
    # build tags object for every word connected to page
    # LOC = GREEN, GPE = BLUE, NUM = PURPLE
    tags = [
        {"id": 1, "keys": [11], "value": "LOC"},
        {"id": 2, "keys": [14], "value": "LOC"},
        {"id": 3, "keys": [15, 16], "value": "GPE"},
        {"id": 4, "keys": [23], "value": "NUM"},
    ]

    return render_template('tagging.html', file=file, text=not_random_text_anymore, tags=tags, tags_json=json.dumps(tags, indent = 4), form=form)
