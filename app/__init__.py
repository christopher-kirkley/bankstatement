"""Define Flask application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask


app = Flask(__name__)


# Set up the configuration
app.config.from_object('config')

# Define database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import the views
from app import views, models

from app.utils import delete_table


# Clear previous values
delete_table()









