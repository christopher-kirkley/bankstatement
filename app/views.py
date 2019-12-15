from app import app
from pathlib import Path
import csv
from datetime import datetime
from app.models import Statement
from app.models import db
from app.models import ImportedCSV
from itertools import islice
from flask import render_template, request, redirect, url_for
from .forms import MyForm
from io import TextIOWrapper


@app.route('/')
@app.route('/index')
def index():
    """Index and home page."""
    return "<h1>This is an app to process bank statements from CSV into tax readable format.</h1>"


@app.route('/import', methods=['get', 'post'])
def import_statement():
    """Route for importing."""

    def import_csv(csv_file, instance):
        """
        Function to import file and load into db.
        Takes argument for csv_file and instance specific.
        """

        """Convert from file object."""
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')

        """Delete all rows from current table."""
        db.session.query(Statement).delete()
        db.session.commit()

        """Skip rows in header."""
        tbl_reader = csv.reader(islice(csv_file, instance.skip, 100), delimiter=',')

        """Iterate over file and add to database."""
        for row in tbl_reader:
            if float(row[2]) < 0:
                """If negative value, add to debit column."""
                db.session.add(Statement(date=datetime.strptime(row[0], '%m/%d/%Y'),
                                         description=row[1],
                                         debit=row[2]))
                db.session.commit()
            elif float(row[2]) > 0:
                """If positive value, add to credit column."""
                db.session.add(Statement(date=datetime.strptime(row[0], '%m/%d/%Y'),
                                         description=row[1],
                                         credit=row[2]))
                db.session.commit()

    """Create instances for use in importing."""
    bofa_csv = ImportedCSV('bank of america', 'row[0]', 'row[1]', 'row[2]', 7)
    wellsfargo_csv = ''
    creditunion_csv = ''

    form = MyForm()
    if form.validate_on_submit():
        csv_file = form.upload.data
        type = form.type.data
        if type == 'bofa_csv':
            import_csv(csv_file, bofa_csv)
        if type == 'wellsfargo_csv':
            import_csv(csv_file, wellsfargo_csv)
        return redirect(url_for('view_statement'))


    return render_template('import.html', form=form)

@app.route('/view', methods=['get', 'post'])
def view_statement():
    """Route for viewing and updating imported statement."""

    """Run a query that selects all fadarom table."""
    query = Statement.query.all()

    """Action on submit."""
    if request.method='POST':
        pass
        #take everything from query and request, and submit to other template?








    return render_template('view.html', query=query)
