from app import app
import csv
from flask import render_template, request, redirect, url_for, send_file, make_response
from io import StringIO

from sqlalchemy import func
from app.models import Statement
from app.models import db
from app.models import ImportedCSV
from app.utils import import_csv, write_csv
from app.settings import tax_categories



@app.route('/')
@app.route('/import', methods=['get', 'post'])
def import_statement():
    """Route for importing."""

    """Create instances for use in importing."""
    bofa_csv = ImportedCSV('bank of america', 'row[0]', 'row[1]', 'row[2]', 7)
    wellsfargo_csv = ''
    creditunion_csv = ''

    # form = MyForm()
    # if form.validate_on_submit():
    #     csv_file = form.upload.data
    #     type = form.type.data
    #     if type == 'bofa_csv':
    #         import_csv(csv_file, bofa_csv)
    #     if type == 'wellsfargo_csv':
    #         import_csv(csv_file, wellsfargo_csv)
    #     return redirect(url_for('view_statement'))

    if request.method == 'POST':
        csv_file = request.files['csv']
        type = request.form.get('type')
        if type == 'bofa_csv':
            import_csv(csv_file, bofa_csv)
        if type == 'wellsfargo_csv':
            import_csv(csv_file, wellsfargo_csv)
        return redirect(url_for('view_statement'))


    return render_template('import.html')

@app.route('/view', methods=['get', 'post'])
def view_statement():
    """Route for viewing and updating imported statement."""

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
        return redirect(url_for('view_statement'))

    return render_template('view.html', query=query, tax_categories=tax_categories)

@app.route('/total', methods=['get', 'post'])
def total():
    """Route to display sum totals."""

    query = db.session.query(Statement.category,
                            func.sum(Statement.debit).label('debit'),
                            func.sum(Statement.credit).label('credit'),
                            (func.sum(Statement.debit) + func.sum(Statement.credit)).label('total'),
                            ).group_by(Statement.category
                                       ).all()

    if request.method == 'POST':
        # Generate temporary file
        si = StringIO()
        cw = csv.writer(si)

        # Write header
        cw.writerow(['category', 'debit total', 'credit total', 'sum total'])
        for row in query:
            cw.writerow([row.category, row.debit, row.credit, row.total])

        # Stream the response as the data is generated.
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

    return render_template('total.html', query=query)

@app.route('/download')
def download():
    query = db.session.query(Statement.category,
                            func.sum(Statement.debit).label('debit'),
                            func.sum(Statement.credit).label('credit'),
                            (func.sum(Statement.debit) + func.sum(Statement.credit)).label('total'),
                            ).group_by(Statement.category
                                       ).all()


@app.route('/settings', methods=['post', 'get'])
def settings():

    if request.method == 'POST':
        if request.form.get('submit') == 'add':
            new_category = request.form.get('add')
            tax_categories.append(new_category)
        if request.form.get('submit') == 'delete':
            category = request.form.get('category')
            tax_categories.remove(category)

    return render_template('settings.html', tax_categories=tax_categories)