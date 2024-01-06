from flask import Flask, Blueprint, render_template
from app.auth.routes import bp as auth_bp
from flask_login import current_user

bp = Blueprint("index", __name__)


def make_routes(app: Flask) -> None:
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")


@bp.route("/")
def index():
    print(current_user.is_authenticated)
    return render_template("index.html")
