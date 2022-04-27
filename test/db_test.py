from tinydb import TinyDB, Query
import unittest


class TinyTest(unittest.TestCase):

    def test_open_db(self):
        player_db = TinyDB('../resource/player_db.json')
        player = Query()
        # check for 'player' attr in db to make sure
        self.assertTrue(player_db.search(player.player.exists()))
        player_db.close()


if __name__ == "__main__":
    unittest.main()
