from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.file_processing.forms import UploadForm
from app.file_processing.tasks import process_file
from app.settings import Config
from app.models import File, Sentences

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

        print(current_user)
        print(current_user.is_authenticated)

        # file_model = File(filename, upload_form.processes.data, 1)
        # file_model.add()

        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(path)
        process_file(filename, upload_form.processes.data)

        return "File is being processed"
    return render_template('upload.html', upload_form=upload_form)


@file_processor_blueprint.route('/view_sentence/<int:sentence_id>', methods=['GET', 'POST'])
def view_db(sentence_id):

    sentence = Sentences.query.filter_by(id=sentence_id).first()
    sentence_words = []

    for words in sentence.words:
        sentence_words.append(words.raw)

    print(sentence_words)
    return json.dumps(sentence_words, ensure_ascii=False)