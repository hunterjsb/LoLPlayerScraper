from flask import Blueprint

from flaskr import db

api_blueprint = Blueprint('api_blueprint', __name__)


@api_blueprint.route('/api/get_player/<name>')
def get_player(name):
    return db.get_player(name)
