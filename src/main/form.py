from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class DownloadForm(FlaskForm):
    url = StringField('Enter address URL')
    submit = SubmitField('Download')