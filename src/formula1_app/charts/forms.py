from wtforms import (
    IntegerField,
    StringField,
    FormField,
    FieldList,
    SelectField,
    SelectMultipleField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    NumberRange,
)
from flask_wtf import FlaskForm


class DriverForm(FlaskForm):
    class Meta:
        csrf = False

    forename = StringField(
        validators=[
            Length(min=0, max=50),
        ]
    )
    surname = StringField(
        validators=[
            Length(min=0, max=50),
        ]
    )


class DriversPerformanceForm(FlaskForm):
    season = IntegerField(
        validators=[
            InputRequired(),
            NumberRange(min=1996, max=2023),
        ]
    )
    drivers = FieldList(FormField(DriverForm), min_entries=1, max_entries=25)


class DriversMostWinsForm(FlaskForm):
    count = IntegerField(
        validators=[
            InputRequired(),
            NumberRange(min=1, max=25),
        ]
    )


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