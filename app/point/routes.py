import json

from flask import Response, flash, redirect, render_template, request, url_for

from app import csrf
from app.integrations.point_api import Point
from app.point import bp
from app.point.forms import PointFilterForm, PointForm


@bp.route("/", methods=["GET", "POST"])
def list():
    """Get a list of Points."""
    form = PointFilterForm()

    filters = {}
    if request.args.get("sort"):
        filters["sort"] = request.args.get("sort", type=str)
        form.sort.data = filters["sort"]
    if request.args.get("name"):
        filters["name"] = request.args.get("name", type=str)
        form.name.data = filters["name"]

    points = Point().list(filters=filters)

    return render_template("list_points.html", title="Points", points=points, form=form)


@bp.route("/new", methods=["GET", "POST"])
def create():
    """Create a new Point."""
    form = PointForm()

    if form.validate_on_submit():
        new_point = Point().create(name=form.name.data, geometry=form.location.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for("point.view", id=new_point["id"]),
                new_point["properties"]["name"],
            ),
            "success",
        )
        return redirect(url_for("point.list"))

    return render_template("create_point.html", title="Create a new point", form=form)


@bp.route("/<uuid:id>", methods=["GET"])
def view(id):
    """Get a Point with a specific ID."""
    point = Point().get(id)

    return render_template("view_point.html", title=point["properties"]["name"], point=point)


@bp.route("/<uuid:id>/edit", methods=["GET", "POST"])
def edit(id):
    """Edit a Point with a specific ID."""
    point = Point().get(id)
    form = PointForm()

    if form.validate_on_submit():
        changed_point = Point().edit(point_id=id, name=form.name.data, geometry=form.location.data)
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for("point.view", id=changed_point["id"]),
                changed_point["properties"]["name"],
            ),
            "success",
        )
        return redirect(url_for("point.list"))
    elif request.method == "GET":
        form.name.data = point["properties"]["name"]
        form.location.data = json.dumps(point["geometry"])

    return render_template(
        "update_point.html",
        title=f"Edit {point['properties']['name']}",
        form=form,
        point=point,
    )


@bp.route("/<uuid:id>/delete", methods=["GET", "POST"])
@csrf.exempt
def delete(id):
    """Delete a Point with a specific ID."""
    point = Point().get(id)

    if request.method == "GET":
        return render_template(
            "delete_point.html",
            title=f"Delete {point['properties']['name']}",
            point=point,
        )
    elif request.method == "POST":
        Point().delete(id)
        flash(f"{point['properties']['name']} has been deleted.", "success")
        return redirect(url_for("point.list"))


@bp.route("/download", methods=["GET"])
def download():
    """Download a list of Points."""
    filters = {}
    if request.args.get("sort"):
        filters["sort"] = request.args.get("sort", type=str)
    if request.args.get("name"):
        filters["name"] = request.args.get("name", type=str)

    points = Point().list(filters=filters, format="csv")
    response = Response(points, mimetype="text/csv", status=200)
    response.headers.set("Content-Disposition", "attachment", filename="points.csv")
    return response
