from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.auth.models import User

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(id: int) -> User:
    return User.query.get(int(id))
