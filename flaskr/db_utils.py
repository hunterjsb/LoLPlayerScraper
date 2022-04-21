from tinydb import TinyDB, Query
from datetime import date


def save_player_data(player_data: dict, db_object: TinyDB, update_age=7):

    player_data['last_updated'] = date.today().timetuple()[0:3]

    name = str(player_data['player'])  # cast to str because father pycharm wants me to
    player = Query()
    instances = db_object.search(player.player == name)
    num_of_instances = len(instances)

    if num_of_instances < 1:
        # Add the player to DB
        db_object.insert(player_data)
    elif num_of_instances == 1:
        if 'last_updated' not in instances[0]:
            # fixing old records
            db_object.update(player_data, player.player == name)
        elif (date.today() - date(*instances[0]['last_updated'])).days >= update_age:
            # Updated the player's data
            db_object.update(player_data, player.player == name)
    else:
        raise IndexError(f"More than one instance of player {name} found in the database")


if __name__ == '__main__':

    test_db = TinyDB('./resource/test_player_db.json')
    save_player_data({"player": "dajor", "role": "mid", "team": "ast", "residency": "eu", "titles": 0,
                      "internation appearances": 0}, test_db)
