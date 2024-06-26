import time

SPORT = 'upcoming'  # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us'  # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h'  # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal'  # decimal | american

DATE_FORMAT = 'iso'  # iso | unix

BET_SIZE = 100

BOOKMAKER_INDEX = 0
NAME_INDEX = 1
ODDS_INDEX = 2
URL_INDEX = 3
FIRST = 0
import json


class Event:
    cache = {}

    def __init__(self, data):
        self.data = data
        self.competition = data['competition']
        self.sport_key = data['sport_key']
        self.id = data['id']

    def find_best_odds(self):
        # number of possible outcomes for a sporting event
        num_outcomes = len(self.data['bookmakers'][FIRST]['markets'][FIRST]['outcomes'])
        self.num_outcomes = num_outcomes

        # finding the best odds for each outcome in each event
        best_odds = [[None, None, float('-inf'), None] for _ in range(num_outcomes)]
        all_odds = [[None, float('-inf')] for _ in range(num_outcomes)]
        # [Bookmaker, Name, Price, Url]

        bookmakers = self.data['bookmakers']
        for index, bookmaker in enumerate(bookmakers):

            # determing the odds offered by each bookmaker
            for outcome in range(num_outcomes):

                # determining if any of the bookmaker odds are better than the current best odds
                bookmaker_odds = float(bookmaker['markets'][FIRST]['outcomes'][outcome]['price'])
                current_best_odds = best_odds[outcome][ODDS_INDEX]

                all_odds[outcome][0] = bookmaker['title']
                all_odds[outcome][1] = bookmaker_odds

                if bookmaker_odds > current_best_odds:
                    best_odds[outcome][BOOKMAKER_INDEX] = bookmaker['title']
                    best_odds[outcome][NAME_INDEX] = bookmaker['markets'][FIRST]['outcomes'][outcome]['name']
                    best_odds[outcome][ODDS_INDEX] = bookmaker_odds
                    best_odds[outcome][URL_INDEX] = bookmaker['url']


        self.all_odds = all_odds
        self.best_odds = best_odds
        return best_odds

    def find_best_odds_with_market_info(self, market_info):
        # number of possible outcomes for a sporting event
        num_outcomes = market_info['number_of_outcomes']
        self.num_outcomes = num_outcomes

        # finding the best odds for each outcome in each event
        best_odds = [[None, None, float('-inf'), None] for _ in range(num_outcomes)]
        all_odds = [[None, float('-inf')] for _ in range(num_outcomes)]
        # [Bookmaker, Name, Price]

        bookmakers = self.data['bookmakers']
        for index, bookmaker in enumerate(bookmakers):

            # skip bookmaker if this does not have this market
            if not contains_market(bookmaker['markets'], market_info['name']):
                continue

            # determing the odds offered by each bookmaker
            for outcome in range(num_outcomes):

                # determining if any of the bookmaker odds are better than the current best odds
                bookmaker_odds = float(bookmaker['markets'][market_info['index']]['outcomes'][outcome]['price'])
                current_best_odds = best_odds[outcome][ODDS_INDEX]


                all_odds[outcome][0] = bookmaker['title']
                all_odds[outcome][1] = bookmaker_odds

                if bookmaker_odds > current_best_odds:
                    best_odds[outcome][BOOKMAKER_INDEX] = bookmaker['title']
                    best_odds[outcome][NAME_INDEX] = bookmaker['markets'][market_info['index']]['outcomes'][outcome][
                        'name']
                    best_odds[outcome][ODDS_INDEX] = bookmaker_odds
                    best_odds[outcome][URL_INDEX] = bookmaker['url']

        self.all_odds = all_odds
        self.best_odds = best_odds
        return best_odds

    def arbitrage(self, best_odds):
        total_arbitrage_percentage = 0
        for odds in best_odds:
            total_arbitrage_percentage += (1.0 / odds[ODDS_INDEX])

        self.total_arbitrage_percentage = total_arbitrage_percentage

        if self.total_arbitrage_percentage > 0:
            self.expected_earnings = (BET_SIZE / total_arbitrage_percentage) - BET_SIZE
        else:
            return False

        profit = (1 - total_arbitrage_percentage) * 100

        return profit

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


def calculate_arbitrage_stakes(stake, odds_a, odds_b, odds_c=None):
    # Calculate the implied probabilities
    implied_prob_a = 1 / odds_a['odd']
    implied_prob_b = 1 / odds_b['odd']

    # Calculate the total implied probability
    total_implied_prob = implied_prob_a + implied_prob_b

    if odds_c is not None:
        implied_prob_c = 1 / odds_c['odd']
        total_implied_prob += implied_prob_c

        # Calculate the stakes for each outcome
        stake_a = (stake / total_implied_prob) * implied_prob_a
        stake_b = (stake / total_implied_prob) * implied_prob_b
        stake_c = (stake / total_implied_prob) * implied_prob_c

        output_string = "{}{} \nStake: {stake_a:.2f}".format(odds_a['name'], odds_a['odd'], stake_a=stake_a)
        output_string += "\n{}{} \nStake: {stake_b:.2f}".format(odds_b['name'], odds_b['odd'], stake_b=stake_b)
        output_string += "\n{}{} \nStake: {stake_c:.2f}".format(odds_c['name'], odds_c['odd'], stake_c=stake_c)

        return output_string
    else:

        # Calculate the stakes for each outcome
        stake_a = (stake / total_implied_prob) * implied_prob_a
        stake_b = (stake / total_implied_prob) * implied_prob_b

        output_string = "For a total stake of: {}\n{}{} \nStake: {stake_a:.2f}".format(stake, odds_a['name'],
                                                                                       odds_a['odd'], stake_a=stake_a)
        output_string += "\n{}{} \nStake: {stake_b:.2f}".format(odds_b['name'], odds_b['odd'], stake_b=stake_b)

        return output_string


def contains_market(markets, name):
    found = [market for market in markets if len(market) != 0 and market['name'] == name]
    return len(found) >= 1


def best_odds_to_names(best_odds):
    if len(best_odds) == 2:
        return str([best_odds[0][1], best_odds[1][1]])
    elif len(best_odds) == 3:
        return str([best_odds[0][1], best_odds[1][1], best_odds[2][1]])
