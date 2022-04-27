from flask import Blueprint
from json import dumps
from tinydb import TinyDB, Query
from datetime import date

from flaskr.bs4scraper import LoLPlayerScraper

api_blueprint = Blueprint('api_blueprint', __name__)

player_db = TinyDB('resource/player_db.json')


@api_blueprint.route('/api/get_player_data/<name>')
def get_player_data(name, update_age=7):

    player = Query()
    instances = player_db.search(player.player == name)
    num_of_instances = len(instances)

    if num_of_instances < 1:
        scraper = LoLPlayerScraper()
        player_data = scraper.get_player_stats(name)
        player_db.insert(player_data)
        return dumps(player_data)

    elif num_of_instances == 1:

        if 'last_updated' not in instances[0]:
            scraper = LoLPlayerScraper()
            player_data = scraper.get_player_stats(name)
            player_db.insert(player_data)
            # fixing old records, remove after all old records are fixed
            player_db.update(player_data, player.player == name)
            return dumps(player_data)

        return dumps(instances[0])

    elif (date.today() - date(*instances[0]['last_updated'])).days >= update_age:
        scraper = LoLPlayerScraper()
        player_data = scraper.get_player_stats(name)
        player_db.update(player_data, player.player == name)
        return dumps(player_data)

    return dumps(instances[0])
    