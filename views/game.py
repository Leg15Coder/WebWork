from flask import current_app as app
from flask import redirect, url_for, render_template, Blueprint
from WEB_YL.data import db_session

blueprint = Blueprint('game', __name__)
