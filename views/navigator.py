from flask import current_app as app
from flask import redirect, url_for, render_template, Blueprint
from WEB_YL.data import db_session

blueprint = Blueprint('navigator', __name__)


@blueprint.route('/about')
def about(name: str):
    pass


@blueprint.route('/scope/<string:name>')
def scope(name: str):
    pass


@blueprint.route('/profession/<string:name>')
def profession(name: str):
    pass
