from flask import Flask
from config import get_config
from app.routes import make_routes
from app.auth import login_manager, bcrypt
from app.database import db


def create_app() -> Flask:
    APP = Flask(__name__)
    APP.config.from_object(get_config())
    db.init_app(APP)
    login_manager.init_app(APP)
    bcrypt.init_app(APP)
    make_routes(APP)
    return APP
