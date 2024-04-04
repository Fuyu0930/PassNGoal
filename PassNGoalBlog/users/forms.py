from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from PassNGoalBlog.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('User name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message = 'Password must match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user =  User.query.filter_by(email = self.email.data).first()
        if user and user != current_user:
            raise ValidationError("Your Email has been registered.")

    def validate_username(self, username):
        user = User.query.filter_by(username = self.username.data).first()
        if user and user != current_user:
            raise ValidationError("Your Username has been registered.")
    
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('User name', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        user =  User.query.filter_by(email = self.email.data).first()
        if user and user != current_user:
            raise ValidationError("Your Email has been registered.")

    def validate_username(self, username):
        user = User.query.filter_by(username = self.username.data).first()
        if user and user != current_user:
            raise ValidationError("Your Username has been registered.")
