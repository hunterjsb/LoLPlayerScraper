from lolplayerscraper import LoLPlayerScraper
import db_utils

if __name__ == "__main__":

    scraper = LoLPlayerScraper()  # instantiate
    player_data = scraper.get_player_stats("perkz")  # look up our boy perkz
    db_utils.save_player_data(player_data)  # save that bad boy
