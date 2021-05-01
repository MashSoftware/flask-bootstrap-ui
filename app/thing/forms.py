from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length


class ThingForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired(message="Enter a name"),
            Length(max=32, message="Name must be 32 characters or fewer"),
        ],
        description="Must be 32 characters or fewer.",
    )
    save = SubmitField("Save")
