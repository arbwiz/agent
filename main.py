from scrapers.betano import betano_tennis_win_match_24h
from scrapers.betclic import betclic_tennis_win_match_24h
from utils import find_arbitrage_bettings
import json

def main():
  betano_data = betano_tennis_win_match_24h()
  betclic_data = betclic_tennis_win_match_24h()

  print('surebets:' + json.dumps(find_arbitrage_bettings(betano_data, betclic_data)[0], indent = 4))
  print('analysed:' + json.dumps(find_arbitrage_bettings(betano_data, betclic_data)[1], indent = 4))

if __name__ == '__main__':
  main()