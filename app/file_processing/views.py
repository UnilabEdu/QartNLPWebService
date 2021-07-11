from flask import Blueprint, render_template, request
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.file_processing.forms import UploadForm
from app.file_processing.tasks import process_file
from app.settings import Config
from app.models.file import File, Pages, Sentences, Words
from app.database import db

import json

import os

file_processor_blueprint = Blueprint('files',
                                     __name__,
                                     template_folder='templates'
                                     )


@file_processor_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    upload_form = UploadForm()

    if upload_form.validate_on_submit():
        file = upload_form.file.data
        filename = secure_filename(file.filename)

        file_model = File(filename, 1, filename)
        file_model.save()

        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(path)
        process_file(file_model.id, filename, upload_form.processes.data)

        return "File is being processed"
    return render_template('upload.html', upload_form=upload_form)


# Temporary pages for debugging
@file_processor_blueprint.route('/view_pages/<int:page_id>', methods=['GET', 'POST'])
def view_page(page_id):

    page = Pages.query.filter_by(id=page_id).first()
    sentences = page.sentences
    print(sentences)

    word_list = []

    return render_template('pages.html', sentences=sentences)


@file_processor_blueprint.route('/view_word/<int:page_id>/<int:word_idx>', methods=['GET', 'POST'])
def view_word(page_id, word_idx):

    page = Pages.query.filter_by(id=page_id).first()
    word = page.word_by_id(word_idx)

    return json.dumps({"word": word.raw, "tag": word.get_ner_tag()}, ensure_ascii=False)


@file_processor_blueprint.route('/find_raw/<int:file_id>/<string:word>', methods=['GET', 'POST'])
def find_raw(file_id, word):

    thing = Words.search_by_raw(file_id, word)
    return render_template('search.html', occurences=thing)


@file_processor_blueprint.route('/find_lemma/<int:file_id>/<string:lemma>', methods=['GET', 'POST'])
def find_lemma(file_id, lemma):

    thing = Words.search_by_lemma(file_id, lemma)
    return render_template('search.html', occurences=thing)


@file_processor_blueprint.route('/find_tags/<int:file_id>/<string:tags>', methods=['GET', 'POST'])
def find_tags(file_id, tags):

    thing = Words.search_by_tag(file_id, tags)
    return render_template('search.html', occurences=thing)


