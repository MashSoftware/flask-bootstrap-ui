from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional


class UserForm(FlaskForm):
    email_address = EmailField(
        "Email address",
        validators=[
            InputRequired(message="Enter your email address"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be 256 characters or fewer"),
        ],
        description="We'll never share your email with anyone else.",
    )
    password = PasswordField(
        "Create a password",
        validators=[
            InputRequired(message="Enter a password"),
            Length(min=8, max=72, message="Password must be between 8 and 72 characters"),
        ],
        description="Must be between 8 and 72 characters.",
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            InputRequired(message="Confirm your password"),
            EqualTo("password", message="Passwords must match."),
        ],
    )


class UserFilterForm(FlaskForm):
    email_address = EmailField("Email address", validators=[Optional()])
