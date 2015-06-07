import os


basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

WTF_CSRF_ENABLED = True
SECRET_KEY = 'somethingimpossibletoguessxd'

RECORDS_PER_PAGE = 3