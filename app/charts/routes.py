from flask import Blueprint, render_template
from flask_login import login_required
from app.charts.models import Chart
from flask import abort

bp = Blueprint("charts", __name__)


@bp.route("/")
@login_required
def index():
    charts = Chart.query.all()
    return render_template(
        "charts/list.html",
        charts=charts,
    )


@bp.route("/chart/<int:chart_id>")
@login_required
def chart_details(chart_id):
    chart = Chart.query.get(chart_id)
    if not chart:
        abort(404)
    return render_template(
        "charts/single.html",
        chart=chart,
    )
