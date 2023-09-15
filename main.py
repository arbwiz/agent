from data_retrievers.betano_scraper import betano_tennis_win_match_24h
from data_retrievers.betclic_scraper import betclic_tennis_win_match_24h
from data_retrievers.betclic_http import betclic_tennis_win_match
from utils import find_arbitrage_bettings
from data_retrievers.aggreagator import get_data
import json

def main():

  data = get_data()
  print(json.dumps(data, indent = 4))
  #debug
  #print('analysed:' + json.dumps(find_arbitrage_bettings(betano_data, betclic_data)[1], indent = 4))

if __name__ == '__main__':
  main()