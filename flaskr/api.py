from flask import Blueprint, request
from json import dumps

from flaskr.lolplayerscraper import LoLPlayerScraper
from flaskr import db_utils

api_blueprint = Blueprint('api_blueprint', __name__)

@api_blueprint.route('/api/get_player_data', methods=['POST'])
def get_player_data():

    if request.method == 'POST':

        player_name = request.args.get('player_name')

        scraper = LoLPlayerScraper()
        player_data = scraper.get_player_stats(player_name)
        db_utils.save_player_data(player_data)

        return dumps(player_data)

    return