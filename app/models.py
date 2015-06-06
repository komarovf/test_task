import re

from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db


likes = db.Table(
    'likes',
    db.Column('answer_id', db.Integer(), db.ForeignKey('answer.id')),
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    _password = db.Column(db.String(64))
    answers = db.relationship('Answer', backref='user', lazy='dynamic')
    questions = db.relationship('Question', backref='user', lazy='dynamic')

    @staticmethod
    def make_valid_login(login):
        return re.sub('[^a-zA-Z0-9_\.]', '', login)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_pass(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        if check_password_hash(self._password, plaintext):
            return True
        return False

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return str(self.login)


class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.String(120))
    date = db.Column(db.DateTime())
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return str(self.body)


class Answer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.String(120))
    date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer(), db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return str(self.body)


