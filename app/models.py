from app import db

class ImportedCSV:
    def __init__(self, name, date, description, amount, skip=0, encoding='utf-8'):
        self.name = name
        self.date = date
        self.description = description
        self.amount = amount
        """Number of rows to skip"""
        self.skip = skip
        """Encoding of file."""
        self.encoding = encoding


"""Define a model for bank statements."""
class Statement(db.Model):
    __tablename__ = 'statement'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    description = db.Column(db.String(300))
    debit = db.Column(db.Numeric(10, 2), default=0)
    credit = db.Column(db.Numeric(10, 2), default=0)
    category = db.Column(db.String(300))


db.create_all()


