from json import dumps
from tinydb import TinyDB, Query
from datetime import date

from flaskr.bs4scraper import LoLPlayerScraper


def get_player(name, update_age=7):

    player_db = TinyDB('resource/player_db.json')
    player = Query()
    instances = player_db.search(player.player == name)
    num_of_instances = len(instances)

    if num_of_instances < 1:
        print('PLAYER NOT FOUND')
        scraper = LoLPlayerScraper()
        player_data = scraper.get_player(name)
        player_db.insert(player_data)
        player_db.close()
        return dumps(player_data)

    elif num_of_instances == 1:
        print('player found....')
        if 'last_updated' not in instances[0]:
            print('not update attr...')
            scraper = LoLPlayerScraper()
            player_data = scraper.get_player(name)
            player_db.insert(player_data)
            # fixing old records, remove after all old records are fixed
            player_db.update(player_data, player.player == name)
            player_db.close()
            return dumps(player_data)

        elif (date.today() - date(*instances[0]['last_updated'])).days >= update_age:
            print('OUT OF DATE')
            scraper = LoLPlayerScraper()
            player_data = scraper.get_player(name)
            player_db.update(player_data, player.player == name)
            player_db.close()
            return dumps(player_data)

        player_db.close()
        return dumps(instances[0])

    elif num_of_instances > 1:
        player_db.close()
        raise IndexError('Multiple instances of player found. Something has gone very wrong.')

    return dumps(instances[0])
