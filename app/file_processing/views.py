from flask import Blueprint, render_template
from werkzeug.utils import secure_filename

from app.file_processing.forms import UploadForm
from app.file_processing.tasks import copy_files
from app.settings import Config

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
        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(path)
        copy_files.delay(path)
        return "File is being processed"
    return render_template('upload.html', upload=upload_form)