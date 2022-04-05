from selenium import webdriver  # WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import json
import re


class LoLPlayerScraper:

    def __init__(self):
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self._load_players()  # loads players.json into self.players

    def _load_players(self):
        with open("resource/players.json") as f:
            self.players = json.load(f)

    def get_player_stats(self, player_name: str):
        # open the player's page
        fandom_wiki_base_url = 'https://lol.fandom.com/wiki/'
        self.driver.get(fandom_wiki_base_url + player_name)

        # find it on the page
        table = self.driver.find_element(By.ID, 'infoboxPlayer')
        print(re.split(r'\W+', table.text))  # EXPERIMENTAL REGEX


if __name__ == "__main__":
    scraper = LoLPlayerScraper()
    scraper.get_player_stats('perkz')

