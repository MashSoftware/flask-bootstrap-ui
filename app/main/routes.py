from app.main import bp
from flask import flash, redirect, render_template, request
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")


@bp.app_errorhandler(HTTPException)
def http_error(error):
    return render_template("error.html", title=error.name, error=error), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    flash("The form you were submitting has expired. Please try again.")
    return redirect(request.full_path)
