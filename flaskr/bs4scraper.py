from bs4 import BeautifulSoup
import requests

from datetime import date
import json

with open('../resource/fandom_attributes.json') as f:
    team_dict, role_dict, region_dict = json.load(f)  # region dict not used atm


class LoLPlayerScraper:
    """
    take in a pro player's IGN and get their role, team, residency, & titles
    returns: dict of the above
    Player's IGN capitalization is often important!
    """
    def __init__(self):
        self.infobox_keywords = ['residency', 'team', 'role']
        self.page = None

    @property
    def soup(self):
        return BeautifulSoup(self.page.text, 'html.parser')

    def get_player_stats(self, player_name: str):
        # first get the page, use default python HTML parser
        fandom_wiki_base_url = 'https://lol.fandom.com/wiki/'
        self.page = requests.get(fandom_wiki_base_url + player_name)

        # get the player table on the player's info page -- retrieve res, team, role
        # we make the ResultSet into a list then filter out the elements that do not contain certain substrings
        # to achieve this I used back-to-back list comprehension... forgive me lord...
        player_table = self.soup.find(id='infoboxPlayer').find_all('tr')  # wierd bs4 `ResultSet` object
        player_attr_list = [x.get_text(separator=' ').lower() for x in player_table]
        player_attr_list = [s for s in player_attr_list if any(xs in s for xs in self.infobox_keywords)]

        # grab the relevant values from the list of strings
        res = player_attr_list[0].split()[1]
        team_list = list(filter('\u2060'.__ne__, player_attr_list[1].split()))[::-1]  # reverse it
        team = team_list[team_list.index('team') - 1]  # bop it
        role = player_attr_list[2].split()[1]

        # translate the scraped terms into standardized abbreviations
        team = team_dict[team]
        role = role_dict[role]

        # now get the tournament results
        self.page = requests.get(fandom_wiki_base_url + player_name + '/Tournament_Results')
        tournament_results = self.soup.find(id='template-reload-1')
        print(tournament_results.prettify())

        return {
            'player': player_name,
            'role': role,
            'team': team,
            'residency': res,
            'appearances': 'appearances',
            'domestic titles': 'd_titles',
            'last_updated': date.today().timetuple()[0:3]
        }


if __name__ == "__main__":
    scraper = LoLPlayerScraper()
    print(scraper.get_player_stats('impact'))
