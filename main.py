from selenium import webdriver  # WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

import json


team_dict = {
    "G2": "G2",
    "FNATIC": "FNC",
    "VITALITY": "VIT",
    "EXCEL": "XL",
    "MISFITS": "MSF",
    "ROGUE": "RGE",
    "ASTRALIS": "AST",
    "MAD": "MAD",
    "SK": "SK",
    "BDS": "BDS",
    "LIQUID": "TL",
    "TSM": "TSM",
    "100": "100",
    "CLG": "CLG",
    "DIGNITAS": "DIG",
    "EVIL": "EG",
    "FLYQUEST": "FLY",
    "GOLDEN": "GG",
    "IMMORTALS": "IMT",
    "CLOUD9": "C9"
}
role_dict = {
    "SUPPORT": "SUP",
    "BOT": "ADC",
    "MID": "MID",
    "JUNGLER": "JG",
    "TOP": "TOP"
}
region_dict = {
    "EUEUROPE": "EU",
    "NANORTH": "NA",
    "TRTURKEY": "TR",
    "CISCIS": "CIS",
    "KRKOREA": "KR",
    "CNCHINA": "CN",
    "OCEOCEANIA": "OCE",
    "LATLATIN": "LAT",
    "LASLAS": "LAT",
    "BRIL": "BR",
    "JPJAPAN": "JP",
    "PCSPCS": "PCS",
    "LMSLMS": "PCS",
    "VNVIETNAM": "VN",
    "SEASEA": "VN",
}


class LoLPlayerScraper:
    """Get player statistics from lol fandom and save locally"""
    def __init__(self):
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self._load_players()  # loads players.json into self.players

    def _load_players(self):
        with open("resource/players.json") as f:
            self.players = json.load(f)

    def get_player_stats(self, player_name: str):
        """
        take in a pro player's IGN and get their role, team, residency and return it as a dict
        Player's IGN capitalization is often important!
        """
        # open the player's page
        fandom_wiki_base_url = 'https://lol.fandom.com/wiki/'
        self.driver.set_page_load_timeout(5)  # fucking fortnite.
        try:
            self.driver.get(fandom_wiki_base_url + player_name)
        except TimeoutException:
            self.driver.execute_script("window.stop();")

        # find it on the page and clean make the table into a list of words
        table = self.driver.find_element(By.ID, 'infoboxPlayer').text.split()
        table = list(filter('\u2060'.__ne__, table))  # remove occurrences of "word join" special character
        table = table[::-1]  # reverse the table, so we get last occurrence of 'Team'

        # build the player dict
        team_str = table[table.index('Team') - 1]
        team = team_dict[team_str.upper()] if team_str.upper() in team_dict else team_str  # my shame
        role_str = table[table.index('Role') - 1]
        role = role_dict[role_str.upper()]
        res_str = table[table.index('Residency') - 1]
        res = region_dict[res_str.upper()]
        return {
            'player': player_name,
            'role': role,
            'team': team,
            'residency': res
        }


if __name__ == "__main__":
    scraper = LoLPlayerScraper()
    print(scraper.get_player_stats('Levi'))
