import logging
from flask import Blueprint, render_template, redirect, flash, url_for
from formula1_app.auth.forms import LoginForm, RegisterForm

from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_login import login_user, logout_user, login_required

from formula1_app.auth import login_manager
from formula1_app.database import db
from formula1_app.auth.models import User

LOGGER = logging.getLogger(__name__)


bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(id: int) -> str:
    return User.query.get(int(id))


@bp.route("/login", methods=("GET", "POST"), strict_slashes=False)
def login() -> str:
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user: User = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("index.index"))
            else:
                flash("Invalid username or password!", "danger")
        except Exception as e:
            LOGGER.error(e)
            flash("An unexpected error has occurred...", "danger")

    return render_template(
        "auth/auth.html",
        form=form,
        btn_action="Login",
    )


@bp.route("/register", methods=("GET", "POST"), strict_slashes=False)
def register() -> str:
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            username = form.username.data
            newuser = User(
                username=username,
                email=email,
                password=password,
            )

            db.session.add(newuser)
            db.session.commit()
            flash("Account succesfully created!", "success")
            return redirect(url_for("auth.login"))

        except InvalidRequestError as e:
            db.session.rollback()
            LOGGER.error(e)
            flash("Something went wrong!", "danger")
        except IntegrityError as e:
            db.session.rollback()
            LOGGER.warning(e)
            flash("User already exists!", "warning")
        except DataError as e:
            db.session.rollback()
            LOGGER.warning(e)
            flash("Invalid Entry", "warning")
        except InterfaceError as e:
            db.session.rollback()
            LOGGER.error(e)
            flash("Error connecting to the database", "danger")
        except DatabaseError as e:
            db.session.rollback()
            LOGGER.error(e)
            flash("Error connecting to the database", "danger")
        except BuildError as e:
            db.session.rollback()
            LOGGER.error(e)
            flash("An error occured!", "danger")
    return render_template(
        "auth/auth.html",
        form=form,
        btn_action="Register",
    )


@bp.route("/logout", strict_slashes=False)
@login_required
def logout() -> str:
    logout_user()
    return redirect(url_for("index.index"))
