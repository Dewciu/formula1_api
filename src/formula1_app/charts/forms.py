from wtforms import (
    IntegerField,
    StringField,
    FormField,
    FieldList,
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
            Length(min=2, max=50),
            InputRequired(),
        ]
    )
    surname = StringField(
        validators=[
            Length(min=2, max=50),
            InputRequired(),
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
