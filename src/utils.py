import requests
import re

betting_types = {
  "1x2": 1,
  "ou": 2,
  "ha": 3,
  "ah": 5,
}

sport_id = {
  "soccer": 2,
  "basketball": 3,
  "baseball": 6,
}

headers = {
    "Referer": "https://www.oddsportal.com/",
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.99 Safari/537.36"
}

def unhash(xhash):
  decoded = "";
  for i in xhash.split("%")[1:]:
    decoded += chr(int(i, 16))
  return decoded

def get_xhash(sport:str, date:int):
  page = requests.get(f"https://www.oddsportal.com/matches/{sport}/{date}/", headers=headers)
  return unhash(re.findall(r'%s":"([^"]+)"' % date, page.text)[0])
