from flask import Flask
from app.auth.routes import bp as auth_bp


def make_routes(app: Flask) -> None:
    app.register_blueprint(auth_bp, url_prefix="/auth")
