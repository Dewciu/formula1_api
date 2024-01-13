from flask import Flask, session
from config import get_config
from formula1_app.routes import make_routes
from formula1_app.auth import login_manager, bcrypt
from formula1_app.database import db


def get_app() -> Flask:
    APP = Flask(__name__)
    APP.config.from_object(get_config())
    bcrypt.init_app(APP)
    db.init_app(APP)
    login_manager.init_app(APP)
    make_routes(APP)
    return APP
