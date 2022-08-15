from flask_babel import gettext as _
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from markupsafe import Markup
from wtforms import StringField, TextAreaField, widgets, SelectMultipleField, RadioField, SubmitField, IntegerField
from wtforms.validators import Length
from wtforms.widgets import html_params


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
    file = FileField(validators=[FileAllowed(['txt', 'docx', 'pdf', 'html'],
                                 message=_('ფაილი არ დამუშავდა. გთხოვთ ატვირთოთ .txt, .pdf, .docx ან .html ფაილი'))])
    processes = MultiCheckboxField(choices=[("lemat", _("ტექსტის ლემატიზაცია")),
                                            # ("token", "ტექსტის ტოკენიზაცია"),
                                            ("freq_dist", _("სიტყვების სიხშირის განაწილება")),
                                            ("remove_html", _("HTML თეგებისგან გასუფთავება")),
                                            ('clean_whitespaces', _('ცარიელი სივრცეების გასუფთავება')),
                                            ('clean_special_characters', _('სიმბოლოებისგან გასუფთავება')),
                                            # ("stop_word", "Stop word-ებისგან გასუფთავება"),
                                            ])
    submit_upload = SubmitField(_('დამუშავება'))


class ExcelForm(FlaskForm):

    file = FileField(validators=[FileAllowed(['xls', 'xlsx'])])
    sheet_name = StringField()
    word_column = StringField(Length(max=2))
    lemma_column = StringField(Length(max=2))
    start_row = IntegerField()

    submit = SubmitField()


class SearchForm(FlaskForm):
    search_field = StringField()
    radio_field = RadioField(choices=[_('ზუსტი ძიება'), _('თავისუფალი ძიება')], default=_('ზუსტი ძიება'))
