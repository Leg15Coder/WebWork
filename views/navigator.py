from flask import current_app as app
from flask import redirect, url_for, render_template, Blueprint
from WEB_YL.data import db_session
from WEB_YL.data.__all_models import Card, CardView

blueprint = Blueprint('navigator', __name__)


@blueprint.route('/about')
def about():
    pass


@blueprint.route('/scope/<int:card>')
def scope(card: int):
    pass


@blueprint.route('/profession/<int:card>')
def profession(card: int):
    params = dict()
    db_sess = db_session.create_session()
    card = db_sess.query(Card).filter(Card.id == card).first()
    params['card'] = CardView(card)
    return render_template("Navigator/profession.html", **params)
