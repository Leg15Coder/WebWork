from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import redirect
from flask import current_app as app
from flask_login import current_user
from functools import wraps


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration
        )
        return email
    except SignatureExpired:
        return False


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            print("You are already authenticated.", "info")
            return redirect("/")
        return func(*args, **kwargs)
    return decorated_function
