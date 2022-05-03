from json import dumps
import datetime
from pymongo import MongoClient

from flaskr.bs4scraper import LoLPlayerScraper


class DBUtil:
    def __init__(self, debug=False):
        self.db = MongoClient('localhost', 27017).openJosh
        self.scraper = LoLPlayerScraper(debug=debug)

    def insert_raw(self, player_data: dict):
        return self.db.players.insert_one(player_data).inserted_id

    def drop_player(self, player_name: str):
        return self.db.player.delete_many({"name": player_name})

    def get_player(self, player_name: str, update_age=7):
        player = self.db.players.find_one({'player': player_name})

        if not player:
            player_data = self.scraper.get_player(player_name)
            self.db.players.insert_one(player_data)
            return dumps(player_data)

        if (datetime.datetime.utcnow() - datetime.datetime(*player['last_updated'])).days >= update_age:
            player_data = self.scraper.get_player(player_name)
            self.db.players.replace_one({player, player_data})
            return dumps(player_data)

        player.pop('_id')
        return player


if __name__ == "__main__":
    entry = {
        "player": "perkz",
        "role": "mid",
        "team": "vit",
        "residency": "eu",
        "appearances": 10,
        "domestic titles": 9,
        "last_updated": datetime.datetime.utcnow()
    }

    dbu = DBUtil(debug=True)
    print(dbu.get_player('perkz'))
