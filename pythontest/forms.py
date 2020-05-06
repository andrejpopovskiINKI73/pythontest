from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pythontest.models import User


class RegistrationForm(FlaskForm):
    username = StringField('UserName',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is taken! Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is taken! Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SettingsForm(FlaskForm):
    keywords = TextAreaField('Keywords',
                           validators=[DataRequired(), Length(min=2, max=500)])
    threshold = IntegerField('Threshold',
                             validators=[DataRequired()])
    submit = SubmitField('Submit')


class SuggestionsForm(FlaskForm):
    url = StringField('RSS feed URL',
                           validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Submit')