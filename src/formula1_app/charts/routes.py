from flask import Blueprint, redirect, url_for, render_template, request, jsonify
from flask_login import login_required
from formula1_app.charts.models import Chart
from flask import abort
from formula1_analytics.drivers.drivers_plots import DriversPlots
from formula1_analytics.drivers.exceptions import DriverNotFoundException, SeasonNotFoundException
from formula1_analytics.drivers.drivers import Drivers
from formula1_analytics.races.races import Races, RacesColumns
from formula1_analytics.results.results import Results, ResultsColumns
from formula1_app.charts.forms import (
    DriversPerformanceForm,
    DriverForm,
    DriversMostWinsForm,
)
from formula1_app.charts.helpers import GetDriversFullnames

import base64
import pandas as pd
from wtforms import IntegerField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, NumberRange
from flask_wtf import FlaskForm


# Define form class directly in this file to make it simpler
class DriverWeatherPerfForm(FlaskForm):
    season = IntegerField(
        validators=[
            InputRequired(),
            NumberRange(min=1996, max=2023),
        ]
    )
    drivers = SelectMultipleField(
        'Drivers',
        choices=[],  # Will be populated dynamically
        validators=[InputRequired()]
    )
    weather_type = SelectField(
        'Weather Type',
        choices=[
            ('rainfall', 'Rainfall'),
            ('track_temp', 'Track Temperature'),
            ('air_temp', 'Air Temperature'),
            ('humidity', 'Humidity'),
            ('pressure', 'Pressure'),
            ('wind_speed', 'Wind Speed'),
        ],
        validators=[InputRequired()]
    )


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


def get_season_drivers(season_year):
    """
    Get a list of drivers who participated in a specific season.
    
    Parameters:
    -----------
    season_year : int
        The season year to filter drivers by
        
    Returns:
    --------
    list of tuples
        (driver_id, driver_name) pairs for drivers who participated in the season
    """
    try:
        # Get races for the season - races are indexed by raceId
        races = Races()
        races_data = races.get_selected_columns(RacesColumns.YEAR)
        season_races = races_data[races_data[RacesColumns.YEAR] == season_year]
        
        if season_races.empty:
            return []
        
        # Get the race IDs from the index
        race_ids = season_races.index.tolist()
        
        # Get results for these races - results has raceId as a column, not an index
        results = Results()
        results_data = results.get_selected_columns(
            ResultsColumns.RACE_ID,
            ResultsColumns.DRIVER_ID
        )
        
        # Get results for the selected races
        season_results = results_data[results_data[ResultsColumns.RACE_ID].isin(race_ids)]
        
        if season_results.empty:
            return []
            
        # Get unique driver IDs
        season_driver_ids = season_results[ResultsColumns.DRIVER_ID].unique()
        
        # Get driver information - drivers are indexed by driverId
        drivers_obj = Drivers()
        driver_names = drivers_obj.get_driver_fullnames()
        
        # Filter to just the drivers from this season and convert to list of tuples
        driver_choices = []
        for driver_id in season_driver_ids:
            if driver_id in driver_names.index:
                name = driver_names.loc[driver_id]
                driver_choices.append((str(driver_id), name))
        
        return sorted(driver_choices, key=lambda x: x[1])  # Sort by driver name
    
    except Exception as e:
        # For debugging
        print(f"Error in get_season_drivers: {e}")
        raise


@bp.route("/chart/driver_performance_weather", methods=["GET", "POST"])
@login_required
def driver_performance_weather():
    chart: Chart = Chart.query.filter_by(identifier="driver_performance_weather").first()
    if not chart:
        abort(404)
    
    # Create form
    form = DriverWeatherPerfForm()
    
    # Check if user requested to load drivers
    load_season = request.args.get('load_season')
    error_message = None
    
    # Process season selection from query parameter
    if load_season and load_season.isdigit():
        season_year = int(load_season)
        try:
            driver_choices = get_season_drivers(season_year)
            if not driver_choices:
                error_message = f"No drivers found for season {season_year}"
            form.drivers.choices = driver_choices
            form.season.data = season_year  # Set the season field
        except Exception as e:
            error_message = f"Error loading drivers: {str(e)}"
            form.drivers.choices = []
    
    # On form submission
    plot = b""
    form_validation_status = None
    
    if request.method == "POST":
        # **IMPORTANT**: Before validating, we need to load the correct driver choices
        # based on the season in the form data
        if 'season' in request.form:
            season_year = int(request.form['season'])
            try:
                driver_choices = get_season_drivers(season_year)
                form.drivers.choices = driver_choices
            except Exception as e:
                error_message = f"Error loading drivers: {str(e)}"
                form.drivers.choices = []
        
        form_validation_status = form.validate_on_submit()
        
        if form_validation_status:
            try:
                # Get selected driver IDs
                selected_driver_ids = form.drivers.data
                if not selected_driver_ids:
                    error_message = "Please select at least one driver."
                else:
                    # Get all drivers (to convert IDs to names)
                    drivers_obj = Drivers()
                    all_drivers = drivers_obj.get_driver_fullnames()
                    
                    # Get selected drivers
                    driver_names = []
                    for driver_id in selected_driver_ids:
                        if int(driver_id) in all_drivers.index:
                            driver_names.append(all_drivers.loc[int(driver_id)])
                    
                    # Generate the plot
                    season_year = int(form.season.data)
                    weather_type = form.weather_type.data
                    
                    # Use the plotting function
                    try:
                        plot = DriversPlots.get_plot_drivers_weather_perf(
                            season_year=season_year,
                            driver_names=driver_names,
                            weather_type=weather_type
                        )
                    except Exception as plot_error:
                        error_message = f"Chart generation failed: {str(plot_error)}"
                        
            except DriverNotFoundException as e:
                error_message = str(e)
            except SeasonNotFoundException as e:
                error_message = str(e)
            except Exception as e:
                error_message = f"Error: {str(e)}"
        else:
            # Form validation failed - show errors
            for field, errors in form.errors.items():
                error_message = f"Field '{field}': {', '.join(errors)}"
    
    return render_template(
        "charts/driver_performance_weather.html",
        chart=chart,
        form=form,
        img_data=base64.b64encode(plot).decode("utf-8") if plot else None,
        error_message=error_message,
        form_validation_status=form_validation_status
    )