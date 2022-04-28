from flask import Blueprint

from flaskr import api_utils

api_blueprint = Blueprint('api_blueprint', __name__)


@api_blueprint.route('/api/get_player_data/<name>')
def get_player_data(name):
    return api_utils.get_player_data(name)
