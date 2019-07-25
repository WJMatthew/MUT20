from bs4 import BeautifulSoup
import pandas as pd
import requests
import warnings;

warnings.simplefilter('ignore')
import time
import re
import json
from tqdm import tqdm_notebook as tqdm

#   Classes:
#       - Player: object to store data for mut card
#
#       - PlayerHandler: class to compile and work with player objects
#

prefix = 'https://www.muthead.com'


class Player:

    def __init__(self, link):
        self.link = link
        self.full_link = prefix + link
        self.json = {}

    def get_ratings(self):
        response = requests.get(self.full_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.soup = soup
        self.get_json()

    def get_json(self):
        tag = self.soup.find('article', class_='mut-card')
        if tag is None:
            print(f'No json found for {self.link}')
        else:
            json_str = tag.attrs['data-props']
            player_dict = json.loads(json_str)
            drops = ['chemistry_maps', 'description', 'external_image_name', 'game', 'long_description']
            _ = [player_dict.pop(drop, None) for drop in drops]
            self.json = player_dict


class PlayerHandler:

    def __init__(self, date, url='https://www.muthead.com/20/players/', pages=0):
        self.url = url
        self.player_list = []
        self.player_links = []
        self.player_dicts = []
        self.player_df = pd.DataFrame
        self.json_out = {}
        self.date = date
        if pages == 0:
            self.n_pages = self.get_num_pages()
        else:
            self.n_pages = pages
        self.print_first_page_link()

    def handle_players(self, pages=None):
        if pages is not None:
            self.n_pages = pages
        self.get_player_links()
        self.make_player_list()

    def get_num_pages(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            n_pages = int(
                soup.find_all('li', class_='pagination__item pagination__item--current')[0].contents[0].split()[-1])
        except:
            print('Error getting number of pages')
            n_pages = 0
        print(f'Number of pages: {n_pages}')
        return n_pages

    def save_player_json(self, dict_list):
        with open(f'player_json_{self.date}', 'w') as fout:
            json.dump(dict_list, fout)

    def get_player_links(self):
        links = []

        for i in range(1, self.n_pages + 1):

            try:
                url = f'{self.url}?page={i}'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')

                for link in soup.findAll('a', attrs={'href': re.compile("20/players/")}):
                    links.append(link.get('href'))

            except Exception:
                print(f'breaking... {len(links)} links gathered.')
                break

        self.player_links = [s for s in links if 'prices' not in s]
        self.player_links = [x for x in self.player_links if x != '/20/players/']
        print(f' {len(self.player_links)} player links gathered.')

    def make_player_list(self):

        for player_link in self.player_links:
            p = Player(player_link)
            self.player_list.append(p)

        for player in tqdm(self.player_list):
            player.get_ratings()
            self.player_dicts.append(player.json)
            time.sleep(1)

        self.save_player_json(self.player_dicts)

    def print_first_page_link(self):
        print(self.url)


class JSONParser:

    abbrevs = {'acceleration': 'ACC', 'agility': 'AGI', 'awareness': 'AWR', 'ball_carrier_vision': 'BCV',
               'block_shedding': 'BKS', 'break_sack': 'BSK', 'break_tackle': 'BTK', 'carrying': 'CAR',
               'catch_in_traffic': 'CIT', 'catching': 'CTH', 'deep_route_running': 'DRR', 'deep_throw_accuracy': 'DAC',
               'elusiveness': 'ELU', 'finesse_moves': 'FNM', 'height': 'HT', 'weight': 'WT', 'hit_power': 'POW',
               'impact_blocking': 'IMP', 'juke_move': 'JKM', 'jumping': 'JMP', 'kick_accuracy': 'KAC',
               'kick_power': 'KPW', 'kick_return': 'KR', 'lead_block': 'LBK', 'man_coverage': 'MCV',
               'medium_route_running': 'MRR', 'medium_throw_accuracy': 'MAC', 'overall': 'OVR',
               'pass_block': 'PBK', 'pass_block_finesse': 'PBF', 'pass_block_power': 'PBP',
               'play_action': 'PAC', 'play_recognition': 'PRC', 'power_moves': 'PWM', 'press': 'PRS',
               'trucking': 'TRK', 'pursuit': 'PUR', 'release': 'RLS',
               'run_block': 'RBK', 'run_block_finesse': 'RBF', 'run_block_power': 'RBP',
               'short_route_running': 'SRR', 'short_throw_accuracy': 'SAC', 'spectacular_catch': 'SPC',
               'speed': 'SPD', 'spin_move': 'SPM', 'stamina': 'STA', 'external_id': 'player_id',
               'stiff_arm': 'SFA', 'strength': 'STR', 'tackle': 'TAK', 'throw_accuracy': 'TAC',
               'throw_power': 'THP', 'throw_under_pressure': 'TUP', 'throwing_on_the_run': 'TOR',
               'toughness': 'TGH'}

    other_keepers = ['image', 'jersey_number', 'last_name', 'last_updated', 'name', 'program_id', 'has_power_up',
                     'quicksell_amount', 'quicksell_currency', 'release_date', 'running_style', 'salary_cap_cost']

    both_traits = ['trait_clutch', 'trait_high_motor', 'trait_penalty', ]
    off_traits = ['trait_aggressive_catches', 'trait_covers_the_ball', 'trait_drops_open_passes',
                  'trait_fights_for_extra_yards', 'trait_makes_sideline_catches', 'trait_possession_catches',
                  'trait_rac_catches', 'trait_makes_sideline_catches']
    qb_traits = ['trait_forces_passes', 'trait_qb_style', 'trait_sense_pressure', 'trait_throw_ball_away',
                 'trait_throws_tight_spiral']
    def_traits = ['trait_big_hitter', 'trait_lb_style', 'trait_plays_ball_in_the_air',
                  'trait_strips_ball', 'trait_utilizes_bull_rush_moves',
                  'trait_utilizes_spin_moves', 'trait_utilizes_swim_moves']

    basics = ['name', 'position', 'program', 'OVR', 'HT', 'WT']
    both = ['SPD', 'ACC', 'AGI', 'AWR', 'CAR', 'STR', 'CTH', 'CIT', 'SPC', 'ELU', 'SPM', 'JKM',
            'SFA', 'TRK', 'IMP', 'JMP', 'STA', 'KR', 'TGH']
    qbs = ['DAC', 'MAC', 'SAC', 'TAC', 'THP', 'TOR', 'TUP', 'PAC']
    offs = ['BCV', 'BSK', 'BTK', 'DRR', 'MRR', 'SRR', 'LBK', 'RBF',
            'RBK', 'RBP', 'RLS', 'PBF', 'PBK', 'PBP']
    defs = ['BKS', 'FNM', 'TAK', 'MCV', 'POW', 'PRC', 'PRS', 'PUR', 'PWM']
    kicks = ['KAC', 'KPW']
    words_for_all = ['image', 'jersey_number', 'last_name', 'player_id', 'program',
                     'quicksell_amount', 'release_date', 'salary_cap_cost', 'team', 'has_power_up']

    position_dict = {'QB': ['QB'],
                     'OFF': ['LT', 'LG', 'C', 'RG', 'RT', 'TE', 'WR', 'HB', 'QB'],
                     'DEF': ['SS', 'FS', 'CB', 'MLB', 'ROLB', 'LOLB', 'RE', 'LE', 'DT'],
                     'ST': ['K', 'P']}

    orders_dict = {'QB': basics + qbs + both + both_traits + qb_traits + offs + defs + words_for_all,
                   'OFF': basics + both + offs + both_traits + off_traits + defs + words_for_all,
                   'DEF': basics + both + defs + both_traits + def_traits + offs + words_for_all,
                   'ST': basics + both + kicks + both_traits + offs + defs + words_for_all}

    def __init__(self, date):
        self.date = date
        self.filename = f'player_json_{date}'
        self.datastore = []
        self.parsed_items = []
        self.df_dict = {}
        self.df = None

    def parse_player_json(self, player_dict):

        traits = [x for x in player_dict if 'trait' in x and player_dict[x] != None]

        return_dict = {}

        for attrib in self.other_keepers:
            return_dict[attrib] = player_dict[attrib]

        for rating_name_long, abbrev in self.abbrevs.items():
            return_dict[abbrev] = player_dict[rating_name_long]

        for t in traits:
            return_dict[t] = player_dict[t]

        return_dict['position'] = player_dict['position']['abbreviation']
        return_dict['program'] = player_dict['program']['description']
        return_dict['team'] = player_dict['team']['abbreviation']
        return return_dict

    def load_json(self, filename=None):
        if filename is None: filename = self.filename
        with open(filename, 'r') as f:
            self.datastore = json.load(f)

    def parse_json_items(self):
        self.parsed_items = [self.parse_player_json(x) for x in self.datastore]

    def add_more_players(self, players_to_add):
        for pta in players_to_add:
            p = Player(pta)
            p.get_ratings()
            parsed = self.parse_player_json(p.json)
            self.parsed_items.append(parsed)

    def jsons_to_dataframe(self):
        self.df = pd.DataFrame(self.parsed_items)

    def save_to_csv(self):

        self.df_dict = {}

        for pos_group, positions in self.position_dict.items():
            self.df_dict[pos_group] = self.df[ self.df['position'].isin(self.position_dict[pos_group])][self.orders_dict[pos_group]]
            self.df_dict[pos_group].reset_index(drop=True).to_csv(f'{self.date}_{pos_group}.csv', index=False)

