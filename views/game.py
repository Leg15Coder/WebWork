from flask import current_app as app
from flask import redirect, url_for, render_template, Blueprint
from flask_login import login_required, current_user
from WEB_YL.data import db_session
from WEB_YL.forms.game import UniteForm
from WEB_YL.data.__all_models import Card, User

blueprint = Blueprint('game', __name__)


class CardView(object):
    def __init__(self, card: Card):
        self.name = card.name
        self.id = card.id
        self.img = f'img/cards/{card.id}.png'
        self.field = card.field
        self.field_img = f'img/fields/{self.field}.png'

    def __repr__(self):
        return f"<CARDVIEW {self.id} {self.name}>"


@blueprint.route('/game', methods=['GET', 'POST'])
def main_game():
    params = dict()
    params['form'] = UniteForm()
    if params['form'].validate_on_submit():
        card1 = params['form'].first
        card2 = params['form'].second
        db_sess = db_session.create_session()
        card = db_sess.query(Card).filter(Card.first_creation_component == card1).filter(
            Card.second_creation_component == card2)
        if not card:
            card = db_sess.query(Card).filter(Card.first_creation_component == card2).filter(
                Card.second_creation_component == card1)
        if not card:
            params['message'] = "К сожалению, мы не можем объединить эти две сферы"
        else:
            pass
    profs = list()
    db_sess = db_session.create_session()
    for card in db_sess.query(User).filter(User.id == current_user.id).one().cards:
        d = CardView(card)
        profs.append(d)
    params['cards'] = profs
    return render_template('Navigator/game.html', **params)
