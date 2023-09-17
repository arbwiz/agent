from utils import calculate_arbitrage_3_websites
from data_retrievers.aggregator import process_data_set
from data_retrievers.twentytwobet import twentytwobet_tennis_win_match
from data_retrievers.esconline import esconline_tennis_win_match_24h
from data_retrievers.esconline import esconline_football
from data_retrievers.betano import betano_football
from data_retrievers.betclic import betclic_football
from data_retrievers.twentytwobet import twentytwobet_football
from utils import print_properly
from utils import compare_strings_with_ratio
import asyncio

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
    
    compare_strings_with_ratio("")

if __name__ == '__main__':
  asyncio.run(main())