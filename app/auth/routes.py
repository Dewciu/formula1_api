import logging
from flask import Blueprint, render_template, redirect, flash, url_for
from app.auth.forms import LoginForm, RegisterForm

from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import check_password_hash

from flask_login import (
    login_user,
)

from app.auth import bcrypt
from app.database import db
from app.auth.models import User

LOGGER = logging.getLogger(__name__)


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template(
        "auth/auth.html",
        form=form,
    )


@bp.route("/register", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            username = form.username.data
            newuser = User(
                username=username,
                email=email,
                password=str(bcrypt.generate_password_hash(password)),
            )

            db.session.add(newuser)
            db.session.commit()
            flash("Account succesfully created!", "success")
            return redirect(url_for("auth.login"))

        except InvalidRequestError:
            db.session.rollback()
            flash("Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash("Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash("Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash("Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash("An error occured!", "danger")
    return render_template(
        "auth/auth.html",
        form=form,
    )
