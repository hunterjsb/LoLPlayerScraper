from flask import Blueprint

from flaskr import db

api_blueprint = Blueprint('api_blueprint', __name__)


@api_blueprint.route('/api/get_player_data/<name>')
def get_player_data(name):
    return db.get_player_data(name)
