from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class UniteForm(FlaskForm):
    first = StringField('Карта 1', validators=[DataRequired()])
    second = StringField('Карта 2', validators=[DataRequired()])
    submit = SubmitField('Объединить')
