from flask import Blueprint, render_template, request
from flask_login import login_required
from formula1_app.charts.models import Chart
from flask import abort
from formula1_analytics.drivers.drivers_plots import DriversPlots
from formula1_analytics.drivers.exceptions import DriverNotFoundException
from formula1_app.charts.forms import DriversPerformanceForm, DriverForm
from formula1_app.charts.helpers import GetDriversFullnames

import base64

bp = Blueprint("charts", __name__)


@bp.route("/")
@login_required
def index() -> str:
    charts = Chart.query.all()
    return render_template(
        "charts/list.html",
        charts=charts,
    )


@bp.route("/chart/<int:chart_id>", methods=["GET", "POST"])
@login_required
def chart_details(chart_id: int) -> str:
    form = DriversPerformanceForm()
    template_form = DriverForm(prefix="drivers-_-")
    plots = DriversPlots()
    chart = Chart.query.get(chart_id)
    plot = b""
    print(request.data)
    if form.validate_on_submit():
        if form.data["drivers"]:
            driver_fullnames = GetDriversFullnames(form.data["drivers"]).get()

        try:
            plot = plots.plot_drivers_season_performance(
                int(form.season.data), driver_fullnames
            )
        except DriverNotFoundException as e:
            return render_template(
                "charts/single.html",
                chart=chart,
                form=form,
                img_data=base64.b64encode(plot).decode("utf-8"),
                _template=template_form,
                driver_not_found_error=e,
            )
    if not chart:
        abort(404)

    return render_template(
        "charts/single.html",
        chart=chart,
        form=form,
        img_data=base64.b64encode(plot).decode("utf-8"),
        _template=template_form,
    )
