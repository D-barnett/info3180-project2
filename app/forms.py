from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import InputRequired, EqualTo
from models import db, User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class registerForm(FlaskForm):
    first_name = StringField('Firstname', validators=[InputRequired()])
    last_name = StringField('Lastname', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm=PasswordField('Confirm password', validators=[InputRequired()])
    
    '''def validate(self):
        check_validate=super(registerForm, self).validate()
        if not check_validate:
            return False
    
        user=User.query.filter(username=self.username.data).first()
        # if username is already in use
        if user:
            self.username.errors.append('This username has already been taken.')
            return False
        return True'''