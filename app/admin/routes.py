from flask import Blueprint, render_template
from flask_login import login_required
from app.admin.helpers import admin_required
from app.charts.models import Chart

bp = Blueprint("admin", __name__)


@bp.route("/")
@login_required
@admin_required
def index() -> str:
    return render_template("admin/manage.html")


@bp.route("/users", strict_slashes=False)
@login_required
@admin_required
def users() -> str:
    return render_template("admin/users.html")


@bp.route("/charts", strict_slashes=False)
@login_required
@admin_required
def charts() -> str:
    charts = Chart.query.all()
    return render_template(
        "admin/charts.html",
        charts=charts,
    )
