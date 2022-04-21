from selenium import webdriver  # WebDriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # RIP secret tech
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.firefox import GeckoDriverManager

import json


with open('resource/fandom_attributes.json') as f:
    team_dict, role_dict, region_dict = json.load(f)


class LoLPlayerScraper:
    """Get player statistics from lol fandom and save locally"""
    def __init__(self):
        service = Service(executable_path=GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)

    def close_driver(self):
        self.driver.quit()

    def get_player_stats(self, player_name: str, close_driver = True):
        """
        take in a pro player's IGN and get their role, team, residency and return it as a dict
        Player's IGN capitalization is often important!
        """
        # open the player's page (Ideally Perkz)
        fandom_wiki_base_url = 'https://lol.fandom.com/wiki/'
        self.driver.set_page_load_timeout(5)  # fucking fortnite.
        try:
            self.driver.get(fandom_wiki_base_url + player_name)
        except TimeoutException:
            self.driver.execute_script("window.stop();")

        # find it on the page and clean make the table into a list of words
        player_stats = self.driver.find_element(By.ID, 'infoboxPlayer').text.split()
        player_stats = list(filter('\u2060'.__ne__, player_stats))  # remove occurrences of "word join" character
        player_stats = player_stats[::-1]  # reverse the table, so we get last occurrence of 'Team'

        try:
            self.driver.get(fandom_wiki_base_url + player_name + '/Tournament_Results')
        except TimeoutException:
            self.driver.execute_script("window.stop();")

        # we could use this instead of the try accept blocks too
        # something is fucked up for the whiteknight page here
        tournament_results = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID,
                                                                                                  "template-reload-1")))
        tournament_results = tournament_results.text.lower().split()
        tournament_results = list(filter('\u2060'.__ne__, tournament_results))  # remove occurrences of \u2060
        appearances = tournament_results.count('msi') + tournament_results.count('worlds')

        # get domestic titles (god save us and god save the queen)
        playoffs = ['playoffs', 'showdown', 'championship']
        regions = ['lec', 'lcs', 'lck', 'lpl']
        d_titles = 0
        for i, word in enumerate(tournament_results):
            if word.startswith('20') and len(word) == 10:
                place = tournament_results[i+1]
                if place == '1':
                    next_ten_words = tournament_results[i + 1:i + 10]  # look at the next ten words
                    if any(_ in next_ten_words for _ in playoffs):
                        if any(_ in next_ten_words for _ in regions):
                            d_titles += 1
                    if 'champions' in next_ten_words and 'preseason' not in next_ten_words:
                        d_titles += 1

        # build the player dictionary
        if 'Team' in player_stats:
            team_str = player_stats[player_stats.index('Team') - 1]
        else:
            team_str = 'FA'
        team = team_dict[team_str.upper()] if team_str.upper() in team_dict else team_str  # my shame
        role_str = player_stats[player_stats.index('Role') - 1]
        role = role_dict[role_str.upper()] if role_str.upper() in role_dict else role_str
        res_str = player_stats[player_stats.index('Residency') - 1]
        res = region_dict[res_str.upper()]

        if close_driver:
            self.driver.quit()

        player_data = {
            'player': player_name,
            'role': role,
            'team': team,
            'residency': res,
            'appearances': appearances,
            'domestic titles': d_titles
        }

        return player_data


if __name__ == "__main__":

    scraper = LoLPlayerScraper()
    scraper.get_player_stats("perkz")
