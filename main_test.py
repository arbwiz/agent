from utils import calculate_arbitrage_3_websites
import json

def main():
  

    odds = [[2.12, 3.25, 2.63],
        [2.00, 3.00, 3.00],
        [2.20, 3.00, 2.80]]

    arbitrage_possibilities = calculate_arbitrage_3_websites(odds)

    print(json.dumps(arbitrage_possibilities, indent=4))

if __name__ == '__main__':
  main()