from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    password_again = PasswordField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
