from app import app
import csv
from flask import render_template, request, redirect, url_for

from sqlalchemy import func
from app.models import Statement
from app.models import db
from app.models import ImportedCSV
from .forms import MyForm
from app.utils import import_csv, write_csv

@app.route('/')
@app.route('/index')
def index():
    """Index and home page."""

    return render_template('index.html')


@app.route('/import', methods=['get', 'post'])
def import_statement():
    """Route for importing."""

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

    tax_categories = ['Ask My Accountant', 'Office', 'Computer', 'Shipping Supplies', ]

    """Run a query that selects all table."""
    query = Statement.query.all()

    """Action on submit."""
    if request.method == 'POST':
        """Query entire table, set category to new value in form."""
        rows = Statement.query.all()
        for row in rows:
            row.category = request.form.get(f'text-{row.id}')
            db.session.commit()
        """Write csv from new table."""
        write_csv()
        return redirect(url_for('total'))

    return render_template('view.html', query=query, tax_categories=tax_categories)

@app.route('/total', methods=['get', 'post'])
def total():
    """Route to display sum totals."""

    query = db.session.query(Statement.category,
                            func.sum(Statement.debit).label('debit'),
                            func.sum(Statement.credit).label('credit')
                            ).group_by(Statement.category
                                       ).all()

    return render_template('total.html', query=query)
