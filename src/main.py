import requests
import pandas as pd
import json
import re
import datetime
import time
from pprint import pprint
from bs4 import BeautifulSoup

from colorama import Fore, Back, Style #CLI Colors
import psutil #Memory Checker

import utils

def get_match():
    
    # match_url = input("Enter URL: ")
    match_url = "https://www.oddsportal.com/basketball/europe/eurobasket/spain-finland-IemGF8oL/"
    match_id = match_url.split("/")[-2:-1][0].split("-")[-1:][0]

    today = datetime.date.today().strftime("%Y%m%d")
    # # sport_input = input("Enter Sport: ")
    sport_input = 'basketball'
    betting_type = 'ha'

    # 추후에 input 으로 변경 -> 프론트단 POST 구현
    version_id = 1
    sport_id = utils.sport_id[sport_input]
    betting_type = utils.betting_types[betting_type]
    scope_id = 1
    target_bookie = utils.bookmaker_id['Pinnacle']

    response = requests.get(match_url, headers=utils.headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    # Home - Away -> ['Home', 'Away']
    match_title = soup.select_one("#col-content > h1").text.split(" - ")
    # t1663082100-4-1-1-1 -> t1663082100 -> 1663082100
    match_date = soup.select_one("#col-content > p.date.datet")['class'][-1:][0].split("-")[0].replace("t","")
    match_date = datetime.datetime.fromtimestamp(int(match_date))
    
    match_info = {
      "Home": match_title[0],
      "Away": match_title[1],
      "Date": match_date
    }
    
    if response.status_code == 200:
        html = response.text
        xhash = utils.unhash(re.findall(r'xhash":"([^"]+)', html)[0])
        time_now_ms = int(round(time.time() * 1000))
        json_url = "http://fb.oddsportal.com/feed/match/" + "%d-%d-%s-%d-%d-%s.dat?_=%s" % \
                    (
                      version_id,
                      sport_id,
                      match_id,
                      betting_type,
                      scope_id,
                      xhash,
                      time_now_ms
                    )
        response = requests.get(json_url, headers=utils.headers)
        odds_data = json.loads(re.findall(r"\.dat',\s({.*})", response.text)[0])
        # Current Odds
        bookie_odds = odds_data['d']['oddsdata']['back'][f'E-{betting_type}-{scope_id}-0-0-0']['odds'][f'{target_bookie}']
        history_cols = odds_data['d']['history']['back'].keys()
        history_dict = dict()
        for idx, cols in enumerate(history_cols):
            history_odds = odds_data['d']['history']['back'][f'{cols}'][f'{target_bookie}']
            data = dict()
            for idx_s, item in enumerate(history_odds):
                value, _, timestamp = item
                row = dict()
                row['timestamp'] = str(datetime.datetime.fromtimestamp(timestamp))
                row['value'] = value
                data[idx_s] = row
            data_sorted = dict(sorted(data.items(), key = lambda item: item[0], reverse=True))
            history_dict[idx] = data_sorted
        with open('history.json', 'w') as file:
          json.dump(history_dict, file, indent=4)
                   
if __name__ == '__main__':
  # Running time
  start_time = time.time()
  
  get_match()
  
  # Memory checking
  p = psutil.Process()
  rss = p.memory_info().rss / 2 ** 20 # Bytes to MB
  print(f"memory usage: {rss: 10.5f} MB")

  print(Back.WHITE + Fore.BLUE + Style.BRIGHT + "RUNNING TIME : " + Style.RESET_ALL + Back.GREEN + Fore.WHITE + Style.BRIGHT + f"{time.time() - start_time} sec" + Style.RESET_ALL)
