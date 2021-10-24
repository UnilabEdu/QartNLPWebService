from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class NerTagForm(FlaskForm):
    ner_tag = SelectField("Choose a tag from the list",
                          choices=[('num', 'NUM'), ('loc', 'LOC')],
                          validators=[DataRequired()])
    submit = SubmitField("Save")
