SPORT = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

BET_SIZE = 100

BOOKMAKER_INDEX = 0
NAME_INDEX = 1
ODDS_INDEX = 2
FIRST = 0
import json
from notifications.telegram import send_telegram_message

class Event:
    def __init__(self, data):
        self.data = data
        self.sport_key = data['sport_key']
        self.id = data['id']
        
    def find_best_odds(self):
        # number of possible outcomes for a sporting event
        num_outcomes = len(self.data['bookmakers'][FIRST]['markets'][FIRST]['outcomes'])
        self.num_outcomes = num_outcomes

        # finding the best odds for each outcome in each event
        best_odds = [[None, None, float('-inf')] for _ in range(num_outcomes)]
        # [Bookmaker, Name, Price]

        bookmakers = self.data['bookmakers']
        for index, bookmaker in enumerate(bookmakers):

            # determing the odds offered by each bookmaker
            for outcome in range(num_outcomes):

                # determining if any of the bookmaker odds are better than the current best odds
                bookmaker_odds = float(bookmaker['markets'][FIRST]['outcomes'][outcome]['price'])
                current_best_odds = best_odds[outcome][ODDS_INDEX]

                if bookmaker_odds > current_best_odds:
                    best_odds[outcome][BOOKMAKER_INDEX] = bookmaker['title']
                    best_odds[outcome][NAME_INDEX] = bookmaker['markets'][FIRST]['outcomes'][outcome]['name']
                    best_odds[outcome][ODDS_INDEX] = bookmaker_odds
                    
        self.best_odds = best_odds
        return best_odds
    
    def arbitrage(self):
        total_arbitrage_percentage = 0
        for odds in self.best_odds:
            total_arbitrage_percentage += (1.0 / odds[ODDS_INDEX])
            
        self.total_arbitrage_percentage = total_arbitrage_percentage
        
        if self.total_arbitrage_percentage > 0:
            self.expected_earnings = (BET_SIZE / total_arbitrage_percentage) - BET_SIZE
        else :
            print("Error with outcome for event:" + str(self.data['name']))
            self.expected_earnings = -1
            return False

        # if the sum of the reciprocals of the odds is less than 1, there is opportunity for arbitrage
        if total_arbitrage_percentage < 1:
            message = '\nevent: ' + str(self.data['name']) 
            + '\nbest_odds: ' 
            + str(self.best_odds) 
            + '\narbitage_percentage: ' 
            + str(self.total_arbitrage_percentage) 
            + '%\n---\n'
            send_telegram_message(message)
            print(message)
            return True
        return False
    
    # converts decimal/European best odds to American best odds
    def convert_decimal_to_american(self):
        best_odds = self.best_odds
        for odds in best_odds:
            decimal = odds[ODDS_INDEX]
            if decimal >= 2:
                american = (decimal - 1) * 100
            elif decimal < 2:
                american = -100 / (decimal - 1)
            odds[ODDS_INDEX] = round(american, 2)
        return best_odds
     
    def calculate_arbitrage_bets(self):
        bet_amounts = []
        for outcome in range(self.num_outcomes):
            individual_arbitrage_percentage = 1 / self.best_odds[outcome][ODDS_INDEX]
            if self.total_arbitrage_percentage > 0:
                bet_amount = (BET_SIZE * individual_arbitrage_percentage) / self.total_arbitrage_percentage
                bet_amounts.append(round(bet_amount, 2))
            else:
                print("Error with outcome for event:" + json.dumps(self.data))
                bet_amount = 0
                break
        
        self.bet_amounts = bet_amounts
        return bet_amounts