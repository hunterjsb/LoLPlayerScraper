import requests
import unittest


class APITest(unittest.TestCase):

    def test_get_player(self):
        player_data = requests.get('http://0.0.0.0:8000/api/get_player/perkz')
        self.assertEqual(player_data.json()['player'], 'perkz', 'Names not equal.')


if __name__ == "__main__":
    unittest.main()
