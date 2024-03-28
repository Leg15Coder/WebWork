from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import redirect
from flask import current_app as app
from flask_login import current_user
from functools import wraps
from .cards import Card
from .db_session import create_session
import json


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


def load_cards(data_file: str) -> None:
    with open(data_file) as f:
        data = json.load(f)
        db_sess = create_session()
        for i in range(6):
            card = db_sess.query(Card).filter(Card.id == (i + 1)).first()
            if not card:
                new = Card()
                new.id = i + 1
                new.name = data[i]['name']
                new.about = data[i]['about']
                new.field = data[i]['field']
                db_sess.add(new)
    db_sess.commit()
