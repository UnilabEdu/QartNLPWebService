import json

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from app.models.file import File
from app.models.ner_tagging import NerTagType
from app.models.ner_tagging import NerTags
from .forms import NerTagForm

tagging_blueprint = Blueprint('tagging',
                              __name__,
                              static_folder='static',
                              url_prefix='/tagging'
                              )


@tagging_blueprint.route('/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
@login_required
def tagging(page_id=0, file_id=0):
    all_types = NerTagType.query.all()
    all_types = [ner_type.title for ner_type in all_types]

    file = File.file_by_id(file_id)
    if file.user_id != current_user.id:
        flash('ამ ფაილზე წვდომა არ გაქვთ')
        return redirect(url_for('files.all_files'))

    page = file.pages[page_id - 1]

    file_id = str(file.id)

    form = NerTagForm()
    form.ner_tag.choices = NerTagType.get_all_nertags()
    current_page_text = page.get_text()

    tags = NerTags.connected_words(page.id)

    return render_template('tagging/tagging.html',
                           file=file, file_id=file_id, page_id=str(page_id),
                           text=current_page_text, form=form,
                           tags=tags, tags_json=json.dumps(tags, indent=4),
                           all_types=all_types)
