from flask import abort
from flask_login import current_user
from functools import wraps


def admin_required(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)

    return wrapper
