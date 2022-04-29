from bs4 import BeautifulSoup
import requests
import pandas as pd

from datetime import date
import json
import csv


class LoLPlayerScraper:
    """
    take in a pro player's IGN and get their role, team, residency, & titles
    returns: dict of the above
    Player's IGN capitalization is often important!
    """

    def __init__(self, debug=False):
        self.infobox_keywords = ['residency', 'team', 'role']
        self.title_keywords = ['playoffs', 'showdown', 'championship']
        self.region_keywords = ['lec', 'lcs', 'lck', 'lpl']
        self.fandom_url = 'https://lol.fandom.com/wiki/'
        self.page = None

        uri = 'resource/fandom_attributes.json' if not debug else '../resource/fandom_attributes.json'
        with open(uri) as f:
            self.team_dict, self.role_dict, self.region_dict = json.load(f)  # region dict not used atm

    @property
    def soup(self):
        return BeautifulSoup(self.page.text, 'html.parser')

    def get_player(self, player_name: str):
        # first get the page, use default python HTML parser
        self.page = requests.get(self.fandom_url + player_name)

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
        team = self.team_dict[team] if team in self.team_dict else team
        role = self.role_dict[role] if role in self.role_dict else role

        # now get the tournament results
        self.page = requests.get(self.fandom_url + player_name + '/Tournament_Results')
        tournament_results = self.soup.find(id='template-reload-1')
        tr_text = tournament_results.get_text().lower()
        appearances = tr_text.count('msi') + tr_text.count('worlds')
        # print(tournament_results.prettify())

        d_titles = 0
        placement_results = tournament_results.find_all(class_="achievements-place")
        for placement in placement_results:
            if placement.text == '1':
                title = placement.next_sibling.a["data-to-titles"].lower()
                if any(_ in title for _ in self.title_keywords) and any(_ in title for _ in self.region_keywords):
                    d_titles += 1
                if 'champions/' in title and 'preseason' not in title:
                    d_titles += 1
        return {
            'player': player_name,
            'role': role,
            'team': team,
            'residency': res,
            'appearances': appearances,
            'domestic titles': d_titles,
            'last_updated': date.today().timetuple()[0:3]
        }

    def get_team(self, team_name: str):
        self.page = requests.get(self.fandom_url + team_name)
        team_table = self.soup.find(id="team-members-players").find_all('td')
        team_player_list = [x.get_text(separator=' ').lower() for x in team_table]
        print(team_player_list)

        print(requests.get("https://docs.google.com/spreadsheets/d/1Y7k5kQ2AegbuyiGwEPsa62e883FYVtHqr6UVut9RC4o/pubhtml#/export?format=csv").text)


if __name__ == "__main__":
    scraper = LoLPlayerScraper(debug=True)
    print(scraper.get_player('perkz'))
