from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.database import db
from app.settings import Config
from app.files.forms import UploadForm, SearchForm
from app.file_processing.tasks import process_file
from app.models.file import File, Pages, Sentences, Words, Statistics, Status


import json
import time
import os
from zipfile import ZipFile

file_views_blueprint = Blueprint('files',
                                 __name__,
                                 template_folder='templates'
                                 )


@file_views_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    upload_form = UploadForm()

    if upload_form.validate_on_submit():
        if upload_form.file.data:
            file = upload_form.file.data
            filename = secure_filename(file.filename)
            title = filename.split(".")[0]

        elif upload_form.text.data and upload_form.name.data:
            filename = secure_filename(upload_form.name.data + ".txt")
            title = upload_form.name.data

        path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), filename)
        duplicate_count = 0

        while os.path.exists(path):
            duplicate_count += 1
            new_title = f"{title}-{duplicate_count}"
            filename = f"{new_title}.txt"
            path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), filename)

        if duplicate_count is not 0:
            title = new_title

        os.makedirs(os.path.dirname(path), exist_ok=True)

        if upload_form.file.data:
            file.save(path)
        elif upload_form.text.data:
            with open(path, 'w', encoding="utf-8") as f:
                f.write(upload_form.text.data)

        file_model = File(title, current_user.id, filename)
        file_model.save()

        file_status = Status(file_model.id, lemmatized="lemat" in upload_form.processes.data, completed=False)
        file_status.save()

        process_file(file_model.id, current_user.id, filename, upload_form.processes.data)

        return "File is being processed"
    return render_template('upload.html', upload_form=upload_form)


@file_views_blueprint.route('/files', defaults={'page_num':1}, methods=['GET', 'POST'])
@file_views_blueprint.route('/files/<int:page_num>', methods=['GET', 'POST'])
@login_required
def all_files(page_num):

    files = File.get_active_files(current_user.id).paginate(per_page=4, page=page_num)

    return render_template('files.html', block_files=files)


@file_views_blueprint.route('/files/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
@login_required
def concrete(file_id, page_id):

    file = File.file_by_id(file_id)
    page = file.pages[page_id-1]
    word_list = page.get_text()

    statistics = Statistics.statistics_for_file(file_id)

    search_form = SearchForm()

    if search_form.validate_on_submit() and search_form.search_field.data:
        return redirect(url_for('files.search', file_id=file_id, word=search_form.search_field.data))

    return render_template('view_file.html', file=file, word_list=word_list, statistics=statistics, search_form=search_form)


@file_views_blueprint.route('/files/<int:file_id>/search/<string:word>', methods=['GET', 'POST'])
@login_required
def search(word, file_id):

    words = Words.search_by_raw(file_id, word).group_by(Words.sentence_id).all()
    sentences = []

    for word in words:
        sentence_object = Sentences.query.get(word[1].id)
        sentence = {
            "raw_text": sentence_object.get_text(),
            "highlight": word[2].raw,
            "page_id": sentence_object.page_id,
        }

        sentences.append(sentence)

    return render_template('details.html', sentences=sentences)


@file_views_blueprint.route('/files/disable_file/<int:file_id>', methods=['GET', 'POST'])
@login_required
def disable_file(file_id):

    file = File.file_by_id(file_id)

    if current_user.id == file.user_id:
        file.disable()

    return redirect(request.referrer)


@file_views_blueprint.route('/files/download_file/<int:file_id>', methods=['GET', 'POST'])
@login_required
def download_file(file_id):

    file = File.file_by_id(file_id)
    file_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), file.title)
    absolute_path = os.path.join(current_app.root_path, "uploads", str(current_user.id))

    if current_user.id == file.user_id:
        with ZipFile(f"{file_path}.zip", 'w') as zipobj:
            zipobj.write(f"{file_path}.txt", f"{file.title}.txt")

            if file.status[0].lemmatized:
                file.create_json()
                zipobj.write(f"{file_path}-lemmatized.json", f"{file.title}-lemmatized.json")

        return send_from_directory(absolute_path, f"{file.title}.zip", as_attachment=True)

    return redirect(url_for('files.all_files'))


# Temporary pages for debugging
@file_views_blueprint.route('/view_pages/<int:page_id>', methods=['GET', 'POST'])
def view_page(page_id):

    page = Pages.query.filter_by(id=page_id).first()
    sentences = page.sentences
    print(sentences)

    word_list = []

    return render_template('pages.html', sentences=sentences)


@file_views_blueprint.route('/view_word/<int:page_id>/<int:word_idx>', methods=['GET', 'POST'])
def view_word(page_id, word_idx):

    page = Pages.query.filter_by(id=page_id).first()
    word = page.word_by_id(word_idx)

    return json.dumps({"word": word.raw, "tag": word.get_ner_tag()}, ensure_ascii=False)


@file_views_blueprint.route('/find_raw/<int:file_id>/<string:word>', methods=['GET', 'POST'])
def find_raw(file_id, word):

    thing = Words.search_by_raw(file_id, word)

    search_results = Pages.query.join(Sentences).join(Words).filter(Pages.file_id==file_id).filter(Words.raw==word).all()
    print(search_results)
    print(len(thing))

    return render_template('search.html', occurences=thing)


@file_views_blueprint.route('/find_lemma/<int:file_id>/<string:lemma>', methods=['GET', 'POST'])
def find_lemma(file_id, lemma):

    thing = Words.search_by_lemma(file_id, lemma)
    return render_template('search.html', occurences=thing)


@file_views_blueprint.route('/find_tags/<int:file_id>/<string:tags>', methods=['GET', 'POST'])
def find_tags(file_id, tags):

    thing = Words.search_by_tag(file_id, tags)
    return render_template('search.html', occurences=thing)


