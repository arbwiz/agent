from scrapers.betano import betano_tennis_win_match_24h

def main():
  betano_data = betano_tennis_win_match_24h()
  print(betano_data)

if __name__ == '__main__':
  main()