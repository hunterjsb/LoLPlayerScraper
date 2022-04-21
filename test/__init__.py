import requests

payload = {'player_name': 'perkz'}
r = requests.post('http://localhost:443/api/get_player_data', params=payload)
print(r.json())
