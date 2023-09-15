from data_retrievers.betano_scraper import betano_tennis_win_match_24h
from data_retrievers.betclic_scraper import betclic_tennis_win_match_24h
from data_retrievers.betclic_http import betclic_tennis_win_match
from utils import find_arbitrage_bettings
from utils import print_properly
from data_retrievers.aggreagator import get_data
from logic.main import run
import json

def main():

  #data = get_data()
  #data_with_at_least_two_bookmakers = list(filter(lambda event: len(event["bookmakers"]) > 1, data['events']))
  
  run()

if __name__ == '__main__':
  main()