import flask
from flask import jsonify

from . import db_session
from .users import Users

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(Users).all()
    return jsonify(
        {
            'user':
                [item.to_dict(only=('login', 'email', 'about')) for item in users]
        }
    )
