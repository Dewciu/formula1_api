from flask import Blueprint, render_template

bp = Blueprint("charts", __name__)


@bp.route("/")
def index():
    return render_template("charts/list.html")
