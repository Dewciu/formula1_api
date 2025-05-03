from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required
from formula1_app.charts.models import Chart
from flask import abort
from formula1_analytics.drivers.drivers_plots import DriversPlots
from formula1_analytics.drivers.exceptions import DriverNotFoundException
from formula1_app.charts.forms import (
    DriversPerformanceForm,
    DriverForm,
    DriversMostWinsForm,
)
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
    chart: Chart = Chart.query.get(chart_id)
    return redirect(url_for(f"charts.{chart.identifier}"))


@bp.route("/chart/most_successful_drivers", methods=["GET", "POST"])
@login_required
def most_successful_drivers():
    chart: Chart = Chart.query.filter_by(identifier="most_successful_drivers").first()
    form = DriversPerformanceForm()
    template_form = DriverForm(prefix="drivers-_-")
    plot = b""
    if form.validate_on_submit():
        if form.data["drivers"]:
            driver_fullnames = GetDriversFullnames(form.data["drivers"]).get()

        try:
            plot = DriversPlots.plot_drivers_season_performance(
                int(form.season.data), driver_fullnames
            )
        except DriverNotFoundException as e:
            return render_template(
                "charts/most_successful_drivers.html",
                chart=chart,
                form=form,
                img_data=base64.b64encode(plot).decode("utf-8"),
                _template=template_form,
                driver_not_found_error=e,
            )
    if not chart:
        abort(404)

    return render_template(
        "charts/most_successful_drivers.html",
        chart=chart,
        form=form,
        img_data=base64.b64encode(plot).decode("utf-8"),
        _template=template_form,
    )


@bp.route("/chart/most_wins_drivers", methods=["GET", "POST"])
@login_required
def most_wins_drivers():
    chart: Chart = Chart.query.filter_by(identifier="most_wins_drivers").first()
    form = DriversMostWinsForm()
    plot = b""
    if form.validate_on_submit():
        plot = DriversPlots.get_plot_drivers_most_wins(int(form.count.data))

    return render_template(
        "charts/most_wins_drivers.html",
        chart=chart,
        form=form,
        img_data=base64.b64encode(plot).decode("utf-8"),
    )

@bp.route("/chart/driver_performance_weather", methods=["GET", "POST"])
@login_required
def driver_performance_weather():
    chart: Chart = Chart.query.filter_by(identifier="driver_performance_weather").first()
    form = DriversMostWinsForm()
    plot = b""
    if form.validate_on_submit():
        plot = DriversPlots.get_plot_drivers_most_wins(int(form.count.data))
    return render_template(
        "charts/driver_performance_weather.html",
        chart=chart,
        form=form,
        img_data=base64.b64encode(plot).decode("utf-8"),
    )
