from flask import current_app as app
from flask import redirect, url_for, render_template, Blueprint
from flask_login import login_required, current_user
from WEB_YL.data import db_session
from WEB_YL.forms.game import UniteForm
from WEB_YL.data.__all_models import Card, User, CardView

blueprint = Blueprint('game', __name__)


@blueprint.route('/game', methods=['GET', 'POST'])
def main_game():
    params = dict()
    params['form'] = UniteForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if params['form'].validate_on_submit():
        card1 = int(params['form'].first.data)
        card2 = int(params['form'].second.data)
        card = db_sess.query(Card).filter(Card.first_creation_component == card1).filter(
            Card.second_creation_component == card2).first()
        if not card:
            card = db_sess.query(Card).filter(Card.first_creation_component == card2).filter(
                Card.second_creation_component == card1).first()
        if not card:
            params['message'] = "К сожалению, мы не можем объединить эти две сферы"
        elif card not in user.cards:
            user.cards.append(card)
            db_sess.merge(user)
            db_sess.commit()
    profs = list()
    for card in user.cards:
        d = CardView(card)
        profs.append(d)
    params['cards'] = profs
    return render_template('Navigator/game.html', **params)
