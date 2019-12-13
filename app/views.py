from app import app
from pathlib import Path
import csv
from datetime import datetime
from app.models import Statement
from app.models import db
from itertools import islice
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    """Index and home page."""
    return "<h1>This is a test of the main page</h1>"


@app.route('/import')
def import_statement():
    """Route for importing."""

    """Define path for data folder."""
    data_folder = Path("/Users/ck/python/data/")

    """Select file to open, change this to get request from form."""
    file_to_open = data_folder / "stmt.csv"

    """Import file and load into db."""
    with open(file_to_open) as csv_file:
        tbl_reader = csv.reader(islice(csv_file, 7, 70), delimiter=',')
        for row in tbl_reader:
            db.session.add(Statement(date=datetime.strptime(row[0], '%m/%d/%Y'),
                                     description=row[1],
                                     amount=row[2]))
            db.session.commit()

    return 'Imported'

@app.route('/view')
def view_statement():
    """Route for viewing and updating imported statement."""

    """Run a query that selects all from table."""
    query = Statement.query.all()


    return render_template('view.html', query=query)
