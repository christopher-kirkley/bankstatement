from app import db

"""Define a model for bank statements."""
class Statement(db.Model):
    __tablename__ = 'statement'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    description = db.Column(db.String(300))
    amount = db.Column(db.Numeric(10, 2))


db.create_all()


