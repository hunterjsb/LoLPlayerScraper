from json import dumps
import datetime
from pymongo import MongoClient
import hashlib


def default_dumps(d: str):  # _id (mongo object) and last_updated (datetime) to str for dumps
    return dumps(d, default=lambda o: str(o))


class ApiDbUtil:
    def __init__(self, debug=False):
        if debug:
            from bs4scraper import LoLPlayerScraper
        else:
            from flaskr.bs4scraper import LoLPlayerScraper  # will run __init__.py

        self.db = MongoClient('localhost', 27017).openJosh
        self.scraper = LoLPlayerScraper(debug=debug)

    def insert_raw_player(self, player_data: dict):
        """insert whole dict as player object, no data validation!"""
        return self.db.players.insert_one(player_data).inserted_id

    def drop_player(self, player_name: str):
        """drop all players of a given name"""
        return self.db.players.delete_many({'player': player_name})

    def get_player(self, player_name: str, update_age=7):
        """look for a player in the DB, if not found, try and get from lol fandom, or update if entry is old"""
        player = self.db.players.find_one({'player': player_name})

        if not player:  # if not in DB
            player_data = self.scraper.get_player(player_name)
            self.db.players.insert_one(player_data)
            return default_dumps(player_data)

        if (datetime.datetime.utcnow() - player['last_updated']).days >= update_age:  # old entry
            player_data = self.scraper.get_player(player_name)
            self.db.players.replace_one({player, player_data})
            return default_dumps(player_data)

        return default_dumps(player)

    def get_team(self, team_name: str, update_age=7):
        """look for a team in the DB, if not found, try and get from lol fandom, or update if entry is old"""
        team = self.db.teams.find_one({'name': team_name})

        if not team:  # if not in DB
            team_data = self.scraper.get_team(team_name)
            self.db.teams.insert_one(team_data)
            return default_dumps(team_data)

        if (datetime.datetime.utcnow() - team['last_updated']).days >= update_age:  # old entry
            team_data = self.scraper.get_team(team_name)
            self.db.players.replace_one({team, team_data})
            return default_dumps(team_data)

        return default_dumps(team)


class UserDbUtil:
    def __init__(self):
        self.db = MongoClient('localhost', 27017).openJosh

    def create_user(self, email: str, password: str, user: str):
        pass

    def delete_user(self, email: str):
        pass

    def check_password(self, email: str, password: str): # return true if the passwords match
        pass


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
