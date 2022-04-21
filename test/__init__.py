import requests

player_name = 'perkz'

r = requests.get('http://localhost:443/api/get_player_data/{}'.format(player_name))
print(r.json())
