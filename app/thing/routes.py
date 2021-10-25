from flask import Response, flash, redirect, render_template, request, url_for

from app import csrf
from app.integrations.thing_api import Thing
from app.thing import bp
from app.thing.forms import ThingFilterForm, ThingForm


@bp.route("/", methods=["GET", "POST"])
def list():
    """Get a list of Things."""
    form = ThingFilterForm()

    filters = {}
    if request.args.get("sort"):
        filters["sort"] = request.args.get("sort", type=str)
        form.sort.data = filters["sort"]
    if request.args.get("name"):
        filters["name"] = request.args.get("name", type=str)
        form.name.data = filters["name"]
    if request.args.get("colour"):
        filters["colour"] = request.args.get("colour", type=str)
        form.colour.data = filters["colour"]

    things = Thing().list(filters=filters)

    return render_template("list_things.html", title="Things", things=things, form=form)


@bp.route("/new", methods=["GET", "POST"])
def create():
    """Create a new Thing."""
    form = ThingForm()

    if form.validate_on_submit():
        new_thing = Thing().create(name=form.name.data, colour=form.colour.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for("thing.view", id=new_thing["id"]), new_thing["name"]
            ),
            "success",
        )
        return redirect(url_for("thing.list"))

    return render_template("create_thing.html", title="Create a new thing", form=form)


@bp.route("/<uuid:id>", methods=["GET"])
def view(id):
    """Get a Thing with a specific ID."""
    thing = Thing().get(id)

    return render_template("view_thing.html", title=thing["name"], thing=thing)


@bp.route("/<uuid:id>/edit", methods=["GET", "POST"])
def edit(id):
    """Edit a Thing with a specific ID."""
    thing = Thing().get(id)
    form = ThingForm()

    if form.validate_on_submit():
        changed_thing = Thing().edit(thing_id=id, name=form.name.data, colour=form.colour.data)
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for("thing.view", id=changed_thing["id"]), changed_thing["name"]
            ),
            "success",
        )
        return redirect(url_for("thing.list"))
    elif request.method == "GET":
        form.name.data = thing["name"]
        form.colour.data = thing["colour"]

    return render_template(
        "update_thing.html",
        title=f"Edit {thing['name']}",
        form=form,
        thing=thing,
    )


@bp.route("/<uuid:id>/delete", methods=["GET", "POST"])
@csrf.exempt
def delete(id):
    """Delete a Thing with a specific ID."""
    thing = Thing().get(id)

    if request.method == "GET":
        return render_template(
            "delete_thing.html",
            title=f"Delete {thing['name']}",
            thing=thing,
        )
    elif request.method == "POST":
        Thing().delete(id)
        flash(f"{thing['name']} has been deleted.", "success")
        return redirect(url_for("thing.list"))


@bp.route("/download", methods=["GET"])
def download():
    """Download a list of Things."""
    filters = {}
    if request.args.get("sort"):
        filters["sort"] = request.args.get("sort", type=str)
    if request.args.get("name"):
        filters["name"] = request.args.get("name", type=str)
    if request.args.get("colour"):
        filters["colour"] = request.args.get("colour", type=str)

    things = Thing().list(filters=filters, format="csv")
    response = Response(things, mimetype="text/csv", status=200)
    response.headers.set("Content-Disposition", "attachment", filename="things.csv")
    return response
