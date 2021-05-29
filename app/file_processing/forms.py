from flask_wtf import FlaskForm
from flask_wtf.file import FileField


class UploadForm(FlaskForm):
    file = FileField()