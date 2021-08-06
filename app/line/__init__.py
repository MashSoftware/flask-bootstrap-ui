from flask import Blueprint

bp = Blueprint("line", __name__, template_folder="../templates/line")

from app.line import routes  # noqa: E402,F401
