from flask import Blueprint, render_template
import json
from .forms import NerTagForm
from app.models.file import File, Pages
from app.models.ner_tagging import NerTags
from app.models.ner_tagging import NerTagType


tagging_blueprint = Blueprint('tagging',
                              __name__,
                              template_folder='templates',
                              static_folder='static',
                              url_prefix='/tagging'
                              )


@tagging_blueprint.route('/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
def test(page_id=0, file_id=0):

    file = File.file_by_id(file_id)
    page = file.pages[page_id - 1]

    file_id = str(file.id)

    form = NerTagForm()
    form.ner_tag.choices = NerTagType.get_all_nertags()
    not_random_text_anymore = page.get_text()  # TODO: rename this variable

    tags = NerTags.connected_words(page.id)

    return render_template('/tagging.html',
                           file=file, file_id=file_id, page_id=str(page_id),
                           text=not_random_text_anymore, form=form,
                           tags=tags, tags_json=json.dumps(tags, indent=4)
                           )


@tagging_blueprint.route('/new/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
def test2(page_id=0, file_id=0):

    # new code

    all_types = NerTagType.query.all()
    all_types = [ner_type.title for ner_type in all_types]
    print(all_types)
    # end

    file = File.file_by_id(file_id)
    page = file.pages[page_id - 1]

    file_id = str(file.id)

    form = NerTagForm()
    form.ner_tag.choices = NerTagType.get_all_nertags()
    not_random_text_anymore = page.get_text()  # TODO: rename this variable

    tags = NerTags.connected_words(page.id)

    return render_template('/tagging2.html',
                           file=file, file_id=file_id, page_id=str(page_id),
                           text=not_random_text_anymore, form=form,
                           tags=tags, tags_json=json.dumps(tags, indent=4),
                           all_types=all_types  # TODO: rename
                           )
