from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class TeamSelectionForm(FlaskForm):
    team = StringField(
        'Team',
        validators = [DataRequired()]
    )
    submit = SubmitField('Submit')