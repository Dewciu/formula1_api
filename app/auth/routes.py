import logging
from flask import Blueprint, render_template
from app.auth.forms import LoginForm, RegisterForm

LOGGER = logging.getLogger(__name__)


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=("GET", "POST"), strict_slashes=False)
def login():
    return render_template("auth/login.html", form=LoginForm())


@bp.route("/register", methods=("GET", "POST"), strict_slashes=False)
def register():
    return render_template("auth/register.html", form=RegisterForm())
