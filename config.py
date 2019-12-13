import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
FLASK_DEBUG = 1
SECRET_KEY = os.environ.get('SECRET_KEY') or 'takeout_mouse_plenty'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False