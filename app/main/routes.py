from app.main import bp
from app.main.forms import CookiesForm
from flask import (
    flash,
    json,
    make_response,
    redirect,
    render_template,
    request,
)
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")


@bp.route("/cookies", methods=["GET", "POST"])
def cookies_page():
    form = CookiesForm()
    # Default cookies policy to reject all categories of cookie
    cookies_policy = {"functional": "no", "analytics": "no"}

    # Create the response up front so we can set the cookie before returning
    response = make_response(render_template("cookies.html", title="Cookies", form=form))

    if form.validate_on_submit():
        print("Form validated on submit")
        # Update cookies policy consent from form data
        print("Setting functional cookie consent to {}".format(form.functional.data))
        cookies_policy["functional"] = form.functional.data
        print("Setting analytics cookie consent to {}".format(form.analytics.data))
        cookies_policy["analytics"] = form.analytics.data

        # Set cookies policy for one year
        print("Setting cookies_policy cookie to {}".format(json.dumps(cookies_policy)))
        response.set_cookie("cookies_policy", json.dumps(cookies_policy), max_age=31557600)

        # Confirm to the user and return response
        flash("You’ve set your cookie preferences.", "success")
        return response
    elif request.method == "GET":
        if request.cookies.get("cookies_policy"):
            # Set cookie consent radios data to current policy
            print("Found existing cookie policy {}".format(request.cookies.get("cookies_policy")))
            cookies_policy = json.loads(request.cookies.get("cookies_policy"))
            print("Setting functional cookie consent radio to existing {}".format(cookies_policy["functional"]))
            form.functional.data = cookies_policy["functional"]
            print("Setting analytics cookie consent radio to existing {}".format(cookies_policy["analytics"]))
            form.analytics.data = cookies_policy["analytics"]
        else:
            # If conset not previously set, use default "no" policy
            print("No existing cookie policy found, using default policy {}".format(cookies_policy))
            print("Setting functional cookie consent radio to default {}".format(cookies_policy["functional"]))
            form.functional.data = cookies_policy["functional"]
            print("Setting analytics cookie consent radio to default {}".format(cookies_policy["analytics"]))
            form.analytics.data = cookies_policy["analytics"]
    return response


@bp.app_errorhandler(HTTPException)
def http_error(error):
    return render_template("error.html", title=error.name, error=error), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    flash("The form you were submitting has expired. Please try again.")
    return redirect(request.full_path)
