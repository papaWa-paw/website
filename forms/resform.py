from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class RecipesForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    description = TextAreaField()
    ingredients = TextAreaField()
    cooking = TextAreaField()
    type = StringField(validators=[DataRequired()])
    picture = FileField(validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('создать')
