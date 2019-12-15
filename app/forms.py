from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email
from wtforms import SubmitField
from werkzeug.utils import secure_filename


class MyForm(FlaskForm):
    """Create form with fields to upload CSV file."""
    upload = FileField('file', validators=[FileRequired(), FileAllowed(['csv'], 'Invalid format, CSV only')])
    type = SelectField('type',
                       choices=[('bofa_csv', 'Bank of America'),
                                ('wellsfargo_csv', 'Wells Fargo'),
                                ('creditunion_csv', 'Credit Union'),
                                ]
                       )
    submit = SubmitField('Upload')

# class Category(FlaskForm):
#     """Create class with fields for tax categories."""
#     category = SelectField('category',
#                        choices=[
#                            ('ask', 'Ask My Accountant'),
#                            ('office', 'Office'),
#                            ('travel', 'Travel'),
#                        ]
#                        )
#     submit = SubmitField('Submit')