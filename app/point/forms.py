from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField
from wtforms.validators import InputRequired, Length, NumberRange, Optional


class PointForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired(message="Enter a name"),
            Length(max=32, message="Name must be 32 characters or fewer"),
        ],
        description="Must be 32 characters or fewer.",
    )
    latitude = FloatField(
        "Latitude",
        validators=[
            InputRequired(message="Enter a latitude"),
            NumberRange(min=-90, max=90, message="Latitude must be between -90 and 90"),
        ],
        description="Must be between -90 and 90."
    )
    longitude = FloatField(
        "Longitude",
        validators=[
            InputRequired(message="Enter a longitude"),
            NumberRange(min=-180, max=180, message="Longitude must be between -180 and 180"),
        ],
        description="Must be between -180 and 180."
    )


class PointFilterForm(FlaskForm):
    sort = SelectField(
        "Sort by",
        validators=[InputRequired()],
        choices=[("name", "Name")],
        default="name",
    )
    name = StringField("Name", validators=[Optional()])
