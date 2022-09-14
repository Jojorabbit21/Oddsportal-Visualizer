import requests
import pandas as pd
import json
import re
import datetime
import time
from pprint import pprint
from bs4 import BeautifulSoup

import utils

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

target_bookie = 417

response = requests.get(match_url, headers=utils.headers)
if response.status_code == 200:
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
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
  # with open('odds.json', 'w', encoding='UTF-8') as f:
  #   json.dump(odds_data, f, ensure_ascii=False, indent=4)
  
  bookie_odds = odds_data['d']['oddsdata']['back'][f'E-{betting_type}-{scope_id}-0-0-0']['odds'][f'{target_bookie}']
  
  history_cols = odds_data['d']['history']['back'].keys()
  for idx, cols in enumerate(history_cols):
    history_odds = odds_data['d']['history']['back'][f'{cols}'][f'{target_bookie}']
    for item in history_odds:
      value, _, timestamp = item
      print(f'{idx} / {datetime.datetime.fromtimestamp(timestamp)} - {value}')
  
  