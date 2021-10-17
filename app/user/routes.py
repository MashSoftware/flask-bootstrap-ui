from app import csrf
from app.integrations.thing_api import User
from app.user import bp
from app.user.forms import UserFilterForm, UserForm
from flask import flash, redirect, render_template, request, url_for


@bp.route("/", methods=["GET", "POST"])
def list():
    """Get a list of Users."""
    form = UserFilterForm()

    filters = {}
    if request.args.get("sort"):
        filters["sort"] = request.args.get("sort", type=str)
        form.sort.data = filters["sort"]
    if request.args.get("email_address"):
        filters["email_address"] = request.args.get("email_address", type=str)
        form.email_address.data = filters["email_address"]

    users = User().list(
        token=request.cookies.get("token"),
        filters=filters,
    )

    return render_template("list_users.html", title="Users", users=users, form=form)


@bp.route("/new", methods=["GET", "POST"])
def create():
    """Create a new User."""
    form = UserForm()

    if form.validate_on_submit():
        new_user = User().create(email_address=form.email_address.data, password=form.password.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for("user.view", id=new_user["id"]), new_user["email_address"]
            ),
            "success",
        )
        return redirect(url_for("user.list"))

    return render_template("create_user.html", title="Create a new user", form=form)


@bp.route("/<uuid:id>", methods=["GET"])
def view(id):
    """Get a User with a specific ID."""
    user = User().get(
        token=request.cookies.get("token"),
        user_id=id,
    )

    return render_template("view_user.html", title=user["email_address"], user=user)


@bp.route("/<uuid:id>/edit", methods=["GET", "POST"])
def edit(id):
    """Edit a User with a specific ID."""
    user = User().get(
        token=request.cookies.get("token"),
        user_id=id,
    )
    form = UserForm()

    if form.validate_on_submit():
        changed_user = User().edit(
            user_id=id,
            email_address=form.email_address.data,
            password=form.password.data,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for("user.view", id=changed_user["id"]),
                changed_user["email_address"],
            ),
            "success",
        )
        return redirect(url_for("user.list"))
    elif request.method == "GET":
        form.email_address.data = user["email_address"]

    return render_template(
        "update_user.html",
        title=f"Edit {user['email_address']}",
        form=form,
        user=user,
    )


@bp.route("/<uuid:id>/delete", methods=["GET", "POST"])
@csrf.exempt
def delete(id):
    """Delete a User with a specific ID."""
    user = User().get(
        token=request.cookies.get("token"),
        user_id=id,
    )

    if request.method == "GET":
        return render_template(
            "delete_user.html",
            title=f"Delete {user['email_address']}",
            user=user,
        )
    elif request.method == "POST":
        User().delete(id)
        flash(f"{user['email_address']} has been deleted.", "success")
        return redirect(url_for("user.list"))
