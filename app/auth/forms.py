from wtforms import (
    StringField,
    PasswordField,
    ValidationError,
)
from wtforms.validators import (
    InputRequired,
    Length,
    Regexp,
    Email,
    EqualTo,
)
from flask_wtf import FlaskForm
from app.auth.models import User


class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(min=3, max=50),
        ]
    )
    password = PasswordField(
        validators=[
            InputRequired(),
            Length(min=8, max=100),
        ]
    )


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField(
        validators=[
            InputRequired(),
            Email(),
            Length(1, 64),
        ]
    )
    password = PasswordField(
        validators=[
            InputRequired(),
            Length(min=8, max=100),
        ]
    )
    password_confirm = PasswordField(
        validators=[
            InputRequired(),
            Length(min=8, max=100),
            EqualTo("password", message="Passwords must match"),
        ]
    )

    def validate_email(self, email: StringField) -> None:
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username: StringField) -> None:
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")
