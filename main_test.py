from utils import calculate_arbitrage_3_websites
from data_retrievers.aggregator import merge_data_sets
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

    """   print(difflib.SequenceMatcher(None, "AIK - Degerfors IF", "AIK Estocolmo - Degerfors IF").ratio())
    print(difflib.SequenceMatcher(None, "AIK Estocolmo", "AIK").ratio())
    print(difflib.SequenceMatcher(None, "Degerfors IF", "Degerfors IF").ratio())
    print(difflib.SequenceMatcher(None, "AIC Estocolmo", "AIK").ratio())
    print(difflib.SequenceMatcher(None, "Degerfors", "Degerfors IF").ratio())

    print(difflib.SequenceMatcher(None, "Sporting Sub-23 - Mafra Sub -23", "Sporting CP Sub-23 - Mafra Sub-23").ratio())
    print(difflib.SequenceMatcher(None, "Portimonense Sub-23", "Sporting Sub-23").ratio())
    print(difflib.SequenceMatcher(None, "Mafra Sub -23", "Santa Clara Sub-23").ratio())


    choices = ["Sporting Sub-23 - Mafra Sub-23", "Portimonense Sub-23 - Santa Clara Sub-23", "Estrela Amadora Sub-23 - Estoril Sub-23", "Gil Vicente FC Sub-23 - FC Vizela Sub-23"]
    print(process.extract("Sporting Sub-23 - Mafra Sub -23", choices, limit=2)) """

    test()
    


def test():
   aggregated_file = open('input/aggregated.json')
   betano_file = open('input/betano.json')

   # returns JSON object as
   # a dictionary
   aggregated = json.load(aggregated_file)
   betano_event = json.load(betano_file)[0]
   #matched_event = get_matched_event(betano_event, aggregated)

   result = merge_data_sets({"events":aggregated}, [betano_event], "football")

   print(result)

if __name__ == '__main__':
  asyncio.run(main())