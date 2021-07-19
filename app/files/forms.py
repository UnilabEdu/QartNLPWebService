from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, widgets, SelectMultipleField
from wtforms.widgets import html_params
from wtforms.validators import Length
from markupsafe import Markup


class CheckboxListWidget(object):

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = []
        for subfield in field:
            html.append('<div %s>%s %s</div>' % (html_params(**kwargs), subfield(), subfield.label))

        return Markup(''.join(html))


class MultiCheckboxField(SelectMultipleField):
    widget = CheckboxListWidget()
    option_widget = widgets.CheckboxInput()


class UploadForm(FlaskForm):
    name = StringField()
    text = TextAreaField(validators=[Length(max=2000)])
    file = FileField(validators=[FileAllowed(['txt'])])
    processes = MultiCheckboxField(choices=[("lemat", "ტექსტის ლემატიზაცია"),
                                            ("token", "ტექსტის ტოკენიზაცია"),
                                            ("pos_tag", "ტექსტის თეგირება"),
                                            ("stop_word", "Stop word-ებისგან გასუფთავება"),
                                            ("freq_dist", "სიტყვების სიხშირის განაწილება")
                                            ])


class SearchForm(FlaskForm):
    search_field = StringField()