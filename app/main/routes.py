from app.main import bp
from flask import render_template
from werkzeug.exceptions import HTTPException


@bp.route("/")
def index():
    return render_template("main/index.html")


@bp.app_errorhandler(HTTPException)
def http_error(error):
    return render_template("error.html", title=error.name, error=error), error.code
