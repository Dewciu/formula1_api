from flask import Blueprint, render_template
from flask_login import login_required
from formula1_app.admin.helpers import admin_required
from formula1_app.charts.models import Chart
from formula1_app.admin.forms import ChartForm

bp = Blueprint("admin", __name__)


@bp.route("/", methods=["GET"])
@login_required
@admin_required
def index() -> str:
    return render_template("admin/manage.html")


@bp.route("/users", methods=["GET", "POST"], strict_slashes=False)
@login_required
@admin_required
def users() -> str:
    return render_template("admin/users.html")


@bp.route("/charts", methods=["GET", "POST"], strict_slashes=False)
@login_required
@admin_required
def charts() -> str:
    charts = Chart.query.all()
    form = ChartForm()
    if form.validate_on_submit():
        # print(form.image.data)
        print(form.image.data)
        # chart = Chart(
        #     title=form.title.data,
        #     filename=form.image.data,
        #     description=form.description.data,
        # )
        # db.session.add(chart)
        # db.session.commit()
        # form.image.save(f"app/static/images/{form.image.data.filename}")
        # flash("Chart added successfully!", "success")

    return render_template(
        "admin/charts.html",
        form=form,
        charts=charts,
    )
