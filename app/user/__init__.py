from flask import Blueprint

bp = Blueprint("user", __name__, template_folder="../templates/user")

from app.user import routes  # noqa: E402,F401
