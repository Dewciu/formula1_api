from flask import Flask, Blueprint, render_template
from app.auth.routes import bp as auth_bp
from app.charts.routes import bp as charts_bp
from app.admin.routes import bp as admin_bp

bp = Blueprint("index", __name__)


def make_routes(app: Flask) -> None:
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(charts_bp, url_prefix="/charts")
    app.register_blueprint(admin_bp, url_prefix="/admin")


@bp.route("/")
def index() -> str:
    return render_template("index.html")
