from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, SubmitField, StringField, EmailField, BooleanField
from wtforms.validators import DataRequired
import wtforms


class RegisterForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    about = TextAreaField('About me')
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class TaskSendForm(FlaskForm):
    code = TextAreaField('Code')
    file = wtforms.FileField('File')
    submit = SubmitField('Submit')


class InterprerForm(FlaskForm):
    code = TextAreaField('Code')
    submit = SubmitField('Run')
    output = TextAreaField('Result')
