from json import dumps
import datetime
from pymongo import MongoClient


class DBUtil:
    def __init__(self, debug=False):
        if debug:
            from bs4scraper import LoLPlayerScraper
        else:
            from flaskr.bs4scraper import LoLPlayerScraper  # will run __init__.py

        self.db = MongoClient('localhost', 27017).openJosh
        self.scraper = LoLPlayerScraper(debug=debug)

    def insert_raw(self, player_data: dict):
        """insert whole dict as player object, no data validation!"""
        return self.db.players.insert_one(player_data).inserted_id

    def drop_player(self, player_name: str):
        """drop all players of a given name"""
        return self.db.players.delete_many({'player': player_name})

    def get_player(self, player_name: str, update_age=7):
        """look for a player in the DB, if not found, try and get from lol fandom, or update if entry is old"""
        player = self.db.players.find_one({'player': player_name})

        def default_dump(d: str):  # _id (mongo object) and last_updated (datetime) to str for dumps
            return dumps(d, default=lambda o: str(o))

        if not player:  # if not in DB
            player_data = self.scraper.get_player(player_name)
            self.db.players.insert_one(player_data)
            return default_dump(player_data)

        if (datetime.datetime.utcnow() - player['last_updated']).days >= update_age:  # old entry
            player_data = self.scraper.get_player(player_name)
            self.db.players.replace_one({player, player_data})
            return default_dump(player_data)

        return default_dump(player)


if __name__ == "__main__":
    entry = {  # for testing .insert_raw method
        "player": "perkz",
        "role": "mid",
        "team": "vit",
        "residency": "eu",
        "appearances": 10,
        "domestic titles": 9,
        "last_updated": datetime.datetime.utcnow()
    }

    dbu = DBUtil(debug=True)
    print(dbu.get_player('impact'))
