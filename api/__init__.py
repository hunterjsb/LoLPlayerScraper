from flask import Flask, request
from json import dumps

import lolplayerscraper
import db_utils

app = Flask(__name__)

@app.route('/api/get_player_data', methods = ['POST'])
def get_player_data():

    if request.method == 'POST':

        player_name = request.args.get('player_name')

        scraper = lolplayerscraper.LoLPlayerScraper()
        player_data = scraper.get_player_stats(player_name)
        db_utils.save_player_data(player_data)

        return(dumps(player_data))

    return('Hello world!')

if __name__ == '__main__':

    app.run(port = 8000, debug = True)