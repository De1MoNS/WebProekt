from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange


class MovieForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    year = IntegerField('Год', validators=[Optional(), NumberRange(min=1888, max=2030)])
    genre = StringField('Жанр')
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')


class SeriesForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    year = IntegerField('Год', validators=[Optional(), NumberRange(min=1888, max=2030)])
    seasons = IntegerField('Количество сезонов', validators=[Optional(), NumberRange(min=1)])
    genre = StringField('Жанр')
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
