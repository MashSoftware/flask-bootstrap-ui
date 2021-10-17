from flask.helpers import make_response
from werkzeug.wrappers import response
from app.auth import bp
from app.auth.forms import LogInForm
from app.integrations.thing_api import Auth
from flask import current_app, flash, redirect, render_template, request, url_for


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        token = Auth().login(email_address=form.email_address.data, password=form.password.data)
        response = make_response(redirect(url_for("main.index")))
        response.set_cookie("token", token["token"])
        return response
    return render_template("log_in_form.html", title="Log in", form=form)
