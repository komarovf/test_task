from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import Required, Length, Email
from .models import User


class RegisterForm(Form):
    login = StringField('login', validators=[Required()])
    email = StringField('email', validators=[Required(), Email('Please, enter valid email')])
    password = PasswordField('password', validators=[Required(), Length(min=6, message=('Please give a longer password'))])
    confirm_pass = PasswordField('confirm_pass', validators=[Required()])

    def validate(self):
        if not Form.validate(self):
            return False
        
        if self.login.data != User.make_valid_login(self.login.data):
            self.login.errors.append('Please use letters, numbers, dots and underscores only')
            return False
        
        if self.password.data != self.confirm_pass.data:
            self.confirm_pass.errors.append('Passwords should be identical')
            return False

        user = User.query.filter_by(login=self.login.data).first()
        if user is not None:
            self.login.errors.append('This nickname is already in use')
            return False

        return True


class LoginForm(Form):
    login = StringField('login', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(login=self.login.data).first()
        if user is None:
            self.login.errors.append('Invalid login')
            return False
        
        if not user.is_correct_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True


class AskForm(Form):
    title = StringField('title', validators=[Required()])
    body = TextAreaField('body', validators=[Required()])


class AnswerForm(Form):
    body = TextAreaField('body', validators=[Required()])