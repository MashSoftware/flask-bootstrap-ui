from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
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
    geometry = TextAreaField(
        "Geometry",
        validators=[InputRequired(message="Enter a geometry")],
        description="Must be valid GeoJSON.",
    )


class PointFilterForm(FlaskForm):
    sort = SelectField(
        "Sort by",
        validators=[InputRequired()],
        choices=[("name", "Name")],
        default="name",
    )
    name = StringField("Name", validators=[Optional()])
