from flask import Blueprint

bp = Blueprint("polygon", __name__, template_folder="../templates/polygon")

from app.polygon import routes  # noqa: E402,F401
