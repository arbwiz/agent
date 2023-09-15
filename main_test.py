from utils import calculate_arbitrage_3_websites
from data_retrievers.aggreagator import process_data_set
from utils import print_properly

def main():
  

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


    aggregated = []

    aggregated = process_data_set(aggregated, betano_data)

    aggregated = process_data_set(aggregated, betclic_data)

    print_properly(aggregated)

    #arbitrage_possibilities = calculate_arbitrage_3_websites(odds)

    #print(json.dumps(arbitrage_possibilities, indent=4))

if __name__ == '__main__':
  main()