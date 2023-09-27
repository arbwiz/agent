from utils import calculate_arbitrage_3_websites
from data_retrievers.aggregator import merge_data_sets, get_football_data, get_tennis_data
from data_retrievers.twentytwobet import twentytwobet_tennis_win_match
from data_retrievers.esconline import esconline_tennis_win_match_24h
from data_retrievers.esconline import esconline_football
from data_retrievers.betano import betano_football
from data_retrievers.betclic import betclic_football
from data_retrievers.twentytwobet import twentytwobet_football
from utils import print_properly
from utils import compare_strings_with_ratio
import difflib
import asyncio
from thefuzz import process
import json
from data_retrievers.aggregator import get_matched_event
from data_retrievers.aggregator import merge_data_sets
from data_retrievers.lebull import lebull_football, lebull_tennis
from data_retrievers.bwin import bwin_football, bwin_tennis
from model.event import calculate_arbitrage_stakes

async def main():
  
   betano_data = [
      {
         'bookmaker': 'betano',
         'name': 'Djokovic - Medvedev',
         'selections': [
            {
               'name': 'Djokovic',
               'price': 1.5
            },
            {
               'name': 'Medvedev',
               'price': 2
            }
         ]
      },
      {
         'bookmaker': 'betano',
         'name': 'Ruud - Tsitsipas',
         'selections': [
            {
               'name': 'Ruud',
               'price': 1.3
            },
            {
               'name': 'Tsitsipas',
               'price': 2.5
            }
         ]
      }
   ]

   betclic_data = [
      {
         'bookmaker': 'betclic',
         'name': 'N. Djokovic vs D. Medvedev',
         'selections': [
            {
               'name': 'Djokovic',
               'price': 1.2
            },
            {
               'name': 'Medvedev',
               'price': 2.3
            }
         ]
      }
   ]

    #await esconline_football()

    #arbitrage_possibilities = calculate_arbitrage_3_websites(odds)

    #print(json.dumps(arbitrage_possibilities, indent=4))

    #twentytwobet_football()

   # message = calculate_arbitrage_stakes(100, {
   #    'name': "name a",
   #    'odd': 2
   #    },
   #    {
   #    'name': "name b",
   #    'odd': 4
   #    },
   #    {
   #    'name': "name c",
   #    'odd': 5
   #    })
   # result = lebull_tennis()
   # print(result)
   await get_football_data()
   await get_tennis_data()


def test():
   aggregated_file = open('output/aggregated_tennis.json')
   betano_file = open('output/esconline_tennis.json')

   # returns JSON object as
   # a dictionary
   aggregated = json.load(aggregated_file)
   betano_event = json.load(betano_file)[0]
   #matched_event = get_matched_event(betano_event, aggregated)

   result = merge_data_sets({"events":aggregated}, [betano_event], "football")

   print(result)

if __name__ == '__main__':
  asyncio.run(main())