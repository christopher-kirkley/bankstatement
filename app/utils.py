import csv
from io import TextIOWrapper
from itertools import islice
from datetime import datetime

from app.models import db, Statement


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


def write_csv():
    """Function to export a CSV file from a query of table."""

    with open('export.csv', 'w') as f:
        out = csv.writer(f)
        out.writerow(['date', 'description', 'debit', 'credit', 'category'])
        for row in Statement.query.all():
            out.writerow([row.date, row.description, row.debit, row.credit, row.category])


def delete_table():
    """Delete all rows from current table."""

    db.session.query(Statement).delete()
    db.session.commit()

