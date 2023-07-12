from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class PokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Search')

class SignUpForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField("Confirm your password", [DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField('Login')