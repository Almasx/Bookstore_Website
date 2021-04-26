from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired, FileAllowed
GENRE_LIST = [(1, 'Poetry'), (2, 'Fantasy'), (3, 'Science Fiction'),
              (4, 'Mystery'), (5, 'Biography'), (6, 'Drama')]


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remeber me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    photo = FileField(
        validators=[FileAllowed(['jpg', 'png'], 'Image only!'), FileRequired('File was empty!')])
    about = StringField("About", widget=TextArea(), validators=[DataRequired()])
    year = IntegerField("Year published", validators=[DataRequired()])
    genre = SelectField("Genre", choices=GENRE_LIST, validators=[DataRequired()], coerce=int)
    price = FloatField("Price", validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddOrderForm(FlaskForm):
    amount = IntegerField("Amount", validators=[DataRequired()])
    submit = SubmitField('Submit')