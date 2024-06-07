from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    genre = SelectField('Genre', coerce=int)
    year = StringField('Year', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    cover = FileField('Cover')
    submit = SubmitField('Save')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[('5', 'Отлично'), ('4', 'Хорошо'), ('3', 'Удовлетворительно'), ('2', 'Неудовлетворительно'), ('1', 'Плохо'), ('0', 'Ужасно')], validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit')
