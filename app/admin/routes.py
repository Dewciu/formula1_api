from flask import Blueprint, render_template
from flask_login import login_required
from app.admin.helpers import admin_required

bp = Blueprint("admin", __name__)


@bp.route("/")
@login_required
@admin_required
def index() -> str:
    return render_template("admin/manage.html")


@bp.route("/users", strict_slashes=False)
@login_required
@admin_required
def manage_users() -> str:
    return render_template("admin/users.html")


@bp.route("/charts", strict_slashes=False)
@login_required
@admin_required
def manage_charts() -> str:
    return render_template("admin/manage.html")
