from app import csrf
from app.integrations.thing_api import ThingAPI
from app.thing import bp
from app.thing.forms import ThingForm
from flask import flash, redirect, render_template, request, url_for


@bp.route("/", methods=["GET", "POST"])
def list():
    """Get a list of Things."""
    thing_api = ThingAPI()
    name_query = request.args.get("name", type=str)

    if name_query:
        things = thing_api.list(name=name_query)
    else:
        things = thing_api.list()

    return render_template("thing/list_thing.html", title="Things", things=things)


@bp.route("/new", methods=["GET", "POST"])
def create():
    """Create a new Thing."""
    thing_api = ThingAPI()
    form = ThingForm()

    if form.validate_on_submit():
        new_thing = thing_api.create(name=form.name.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for("thing.view", id=new_thing["id"]), new_thing["name"]
            ),
            "success",
        )
        return redirect(url_for("thing.list"))

    return render_template("thing/create_thing.html", title="Create a new thing", form=form)


@bp.route("/<uuid:id>", methods=["GET"])
def view(id):
    """Get a Thing with a specific ID."""
    thing_api = ThingAPI()
    thing = thing_api.view(id)

    return render_template("thing/view_thing.html", title=thing["name"], thing=thing)


@bp.route("/<uuid:id>/edit", methods=["GET", "POST"])
def edit(id):
    """Edit a Thing with a specific ID."""
    thing_api = ThingAPI()
    thing = thing_api.view(id)
    form = ThingForm()

    if form.validate_on_submit():
        changed_thing = thing_api.edit(thing_id=id, name=form.name.data)
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for("thing.view", id=changed_thing["id"]), changed_thing["name"]
            ),
            "success",
        )
        return redirect(url_for("thing.list"))
    elif request.method == "GET":
        form.name.data = thing["name"]

    return render_template(
        "thing/update_thing.html",
        title="Edit {}".format(thing["name"]),
        form=form,
        thing=thing,
    )


@bp.route("/<uuid:id>/delete", methods=["GET", "POST"])
@csrf.exempt
def delete(id):
    """Delete a Thing with a specific ID."""
    thing_api = ThingAPI()
    thing = thing_api.view(id)

    if request.method == "GET":
        return render_template(
            "thing/delete_thing.html",
            title="Delete {}".format(thing["name"]),
            thing=thing,
        )
    elif request.method == "POST":
        thing_api.delete(id)
        flash("{} has been deleted.".format(thing["name"]), "success")
        return redirect(url_for("thing.list"))
