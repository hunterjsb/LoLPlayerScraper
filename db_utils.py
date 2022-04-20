from tinydb import TinyDB, Query

db = TinyDB('./resource/player_db.json')


def save_player_data(player_data: dict):

	name = str(player_data['player'])  # cast to str because father pycharm wants me to
	player = Query()
	instances = len(db.search(player.player == name))

	if instances < 1:
		db.insert(player_data)
	elif instances == 1:
		db.update(player_data, player.player == name)
	else:
		print(f'More than two instances in the DB for player {name}! Something is wrong.')  # TODO raise error


save_player_data({"player": "perkz", "role": "MID", "team": "VIT", "residency": "EU", "appearances": 100, "domestic titles": 99})
	