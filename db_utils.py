import tinydb

def load_players(self):

	self.players = self.player_db.all()


def save_player_data(self):

	# TODO use tinydb query for this. I'm crying rn because it's so bad
	for item in self.player_db.all():

		# TODO option to delete the current data and replace it with new data for player updates
		if item == self.player_data:

			print("Player '{}' already exists in database".format(self.player_data['player']))
			return

	self.player_db.insert(self.player_data)

	