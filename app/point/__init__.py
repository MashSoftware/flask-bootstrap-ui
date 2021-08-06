from flask import Blueprint

bp = Blueprint("point", __name__, template_folder="../templates/point")

from app.point import routes  # noqa: E402,F401
