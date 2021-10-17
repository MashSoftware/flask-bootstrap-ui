from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired, Length


class LogInForm(FlaskForm):
    email_address = EmailField(
        "Email address",
        validators=[
            InputRequired(message="Enter an email address"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be 256 characters or fewer"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Enter a password"),
            Length(min=8, max=72, message="Password must be between 8 and 72 characters"),
        ],
        description="Must be between 8 and 72 characters.",
    )
