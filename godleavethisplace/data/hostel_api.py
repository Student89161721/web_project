import flask
from flask import jsonify, make_response
from requests import  request
from . import db_session
from .hostels import Hostel

blueprint = flask.Blueprint(
    'hostel_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/hostels')
def get_news():
    db_sess = db_session.create_session()
    hostel = db_sess.query(Hostel).all()
    print(hostel)
    return jsonify(
        {
            'hostels':
                [item.to_dict(only=('Title', 'Description', 'Email'))
                 for item in hostel]
        }
    )

@blueprint.route('/api/hostels/<int:hostels_id>', methods=['GET'])
def get_one_news(hostels_id):
    db_sess = db_session.create_session()
    hostels = db_sess.query(Hostel).get(hostels_id)
    if not hostels:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'news': hostels.to_dict(only=(
                'Title', 'Description', 'Email', 'Cell_phones'))
        }
    )

@blueprint.route('/api/hostels', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    #придумайте здесь что нибудь
    news = Hostel(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})

@blueprint.route('/api/hostels/<int:hostels_id>', methods=['DELETE'])
def delete_news(hostels_id):
    db_sess = db_session.create_session()
    hostel = db_sess.query(Hostel).get(hostels_id)
    if not hostel:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(hostel)
    db_sess.commit()
    return jsonify({'success': 'OK'})