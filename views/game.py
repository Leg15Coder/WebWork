from flask import current_app as app
from flask import redirect, url_for, render_template, Blueprint
from WEB_YL.data import db_session
from WEB_YL.forms.game import UniteForm

blueprint = Blueprint('game', __name__)


@blueprint.route('/game')
def main_game():
    params = dict()
    params['form'] = UniteForm()
    if params['form'].validate_on_submit():
        pass
    return render_template('Navigator/game.html', **params)
