from flask import current_app as app
from flask import jsonify, Blueprint, make_response, request
from WEB_YL.data import db_session
from WEB_YL.data.__all_models import Card, User, KeyAPI
from WEB_YL.data.utils import check_key_limited, update_key_limit
import os

blueprint = Blueprint('api', __name__)


@blueprint.route('/api/cards', methods=['POST'])
def post_cards():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    try:
        db_sess = db_session.create_session()
        key = db_sess.query(KeyAPI).filter(KeyAPI.key == request.json['api_key']).first()
        if not key:
            return make_response(jsonify({'error': 'Undefined API key'}), 400)
        is_admin = key.is_admin
        if not is_admin or not check_key_limited(key):
            return make_response(jsonify({'error': 'Not enough access rights'}), 400)
        card = db_sess.query(Card).filter(Card.id == int(request.json['id'])).first()
        if card:
            file = request.files['file']
            if file and file.filename.split('.')[0] == str(request.json['id']):
                file.save(os.path.join('static/img/cards'), file.filename)
            card.id = int(request.json['id'])
            card.name = str(request.json['name'])
            card.about = str(request.json['about'])
            card.field = str(request.json['field'])
            if 'elements' in request.json and len(request.json['elements']) > 1:
                card.first_creation_component = int(request.json['elements'][0])
                card.second_creation_component = int(request.json['elements'][1])
            db_sess.merge(card)
        else:
            card = Card()
            card.id = int(request.json['id'])
            card.name = str(request.json['name'])
            card.about = str(request.json['about'])
            card.field = str(request.json['field'])
            if 'elements' in request.json and len(request.json['elements']) > 1:
                card.first_creation_component = int(request.json['elements'][0])
                card.second_creation_component = int(request.json['elements'][1])
            db_sess.add(card)
        db_sess.commit()
        update_key_limit(key, -1)
        return make_response(jsonify({'status': 'OK'}), 200)
    except Exception as ex:
        return make_response(jsonify({'error': 'Bad request', 'reason': str(ex)}), 400)


@blueprint.route('/api/cards', methods=['DELETE'])
def delete_cards():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    try:
        db_sess = db_session.create_session()
        key = db_sess.query(KeyAPI).filter(KeyAPI.key == request.json['api_key']).first()
        if not key:
            return make_response(jsonify({'error': 'Undefined API key'}), 400)
        is_admin = key.is_admin
        if not is_admin or not check_key_limited(key):
            return make_response(jsonify({'error': 'Not enough access rights'}), 400)
        card = db_sess.query(Card).filter(Card.id == int(request.json['id'])).first()
        if card:
            db_sess.delete(card)
        else:
            update_key_limit(key, -1)
            return make_response(jsonify({'status': 'OK', 'reason': 'card have not been found'}), 204)
        db_sess.commit()
        update_key_limit(key, -1)
        return make_response(jsonify({'status': 'OK'}), 200)
    except Exception as ex:
        return make_response(jsonify({'error': 'Bad request', 'reason': str(ex)}), 400)


@blueprint.route('/api/cards', methods=['GET'])
def get_cards():
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        db_sess = db_session.create_session()
        key = db_sess.query(KeyAPI).filter(KeyAPI.key == request.json['api_key']).first()
        if not key:
            return make_response(jsonify({'error': 'Undefined API key'}), 400)
        if not check_key_limited(key):
            return make_response(jsonify({'error': 'Not enough access rights'}), 400)
        req = dict(request.json)
        cards = db_sess.query(Card)
        answer = {'cards': list()}
        for column in ('name', 'id', 'about', 'elements', 'field'):
            if column in req:
                cards = cards.filter(eval(f"Card.{column}") == req[column])
        for card in cards.all():
            answer['cards'].append(
                {
                    'id': card.id,
                    'name': card.name,
                    'about': card.about,
                    'field': card.field,
                }
            )
            if card.first_creation_component and card.second_creation_component:
                answer['cards'][-1]['elements'] = sorted(
                    (card.first_creation_component, card.second_creation_component))
            else:
                answer['cards'][-1]['elements'] = [card.first_creation_component, card.second_creation_component]
        answer['status'] = 'OK'
        update_key_limit(key, -1)
        db_sess.commit()
        return make_response(jsonify(answer), 200)
    except Exception as ex:
        return make_response(jsonify({'error': 'Bad request', 'reason': str(ex)}), 400)


@blueprint.route('/api/info', methods=['GET'])
def info():
    pass
