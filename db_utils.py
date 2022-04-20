import tinydb

def load_players(self):

	self.players = self.player_db.all()


def save_player_data(self):

	# TODO use tinydb query for this. I'm crying rn because it's so bad
	for item in self.player_db.all():

		if item == self.player_data:

			return

	self.player_db.insert(self.player_data)

	