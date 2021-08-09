from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField
from wtforms.validators import InputRequired, Length, Optional


class PointForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired(message="Enter a name"),
            Length(max=32, message="Name must be 32 characters or fewer"),
        ],
        description="Must be 32 characters or fewer.",
    )
    location = HiddenField(
        "Location",
        validators=[InputRequired(message="Select a location")],
        description="Click on the map to add a location.",
    )


class PointFilterForm(FlaskForm):
    sort = SelectField(
        "Sort by",
        validators=[InputRequired()],
        choices=[("name", "Name")],
        default="name",
    )
    name = StringField("Name", validators=[Optional()])
