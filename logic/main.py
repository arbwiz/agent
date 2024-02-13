import json
import os
import time

import requests

from model.event import Event
from data_retrievers.aggregator import get_tennis_data, get_basket_data, get_volley_data, get_american_football_data
from data_retrievers.aggregator import get_football_data
from notifications.telegram import send_telegram_message

# -5 can be used to test
MIN_PROFIT_MARGIN = 0


async def run(sport):
    match sport:
        case 'football':
            odds_response = await get_football_data()
            handle_football(odds_response)
        case 'tennis':
            odds_response = await get_tennis_data()
            handle_two_way_market(odds_response, 'tennis')
        case 'basket':
            odds_response = await get_basket_data()
            handle_two_way_market(odds_response, 'basket')
        case 'volleyball':
            odds_response = await get_volley_data()
            handle_two_way_market(odds_response, 'volleyball')
        case 'american_football':
            odds_response = await get_american_football_data()
            handle_two_way_market(odds_response, 'american_football')
        case _:
            odds_response = await get_tennis_data()
            handle_two_way_market(odds_response, 'tennis')


def handle_football(odds_response):
    surebets = []
    for data in odds_response:
        event = (Event(data))

        # TODO: refactor from here
        best_odds1 = event.find_best_odds_with_market_info({'name': 'h2h', 'index': 0, 'number_of_outcomes': 3})
        best_odds1[0][1] = '1'
        best_odds1[1][1] = 'x'
        best_odds1[2][1] = '2'

        best_odds2 = event.find_best_odds_with_market_info(
            {'name': 'total_goals_1.5', 'index': 1, 'number_of_outcomes': 2})
        best_odds2[0][1] = 'Over 1.5'
        best_odds2[1][1] = 'Under 1.5'

        best_odds3 = event.find_best_odds_with_market_info(
            {'name': 'total_goals_2.5', 'index': 2, 'number_of_outcomes': 2})
        best_odds3[0][1] = 'Over 2.5'
        best_odds3[1][1] = 'Under 2.5'

        best_odds4 = event.find_best_odds_with_market_info(
            {'name': 'total_goals_3.5', 'index': 3, 'number_of_outcomes': 2})
        best_odds4[0][1] = 'Over 3.5'
        best_odds4[1][1] = 'Under 3.5'

        best_odds5 = event.find_best_odds_with_market_info({'name': '1x 2', 'index': 4, 'number_of_outcomes': 2})
        best_odds5[0][1] = '1x'
        best_odds5[1][1] = '2'

        best_odds6 = event.find_best_odds_with_market_info({'name': '1 x2', 'index': 5, 'number_of_outcomes': 2})
        best_odds6[0][1] = '1'
        best_odds6[1][1] = 'x2'

        best_odds7 = event.find_best_odds_with_market_info({'name': '12 x', 'index': 6, 'number_of_outcomes': 2})
        best_odds7[0][1] = '12'
        best_odds7[1][1] = 'x'

        for best_odds in [['h2h', best_odds1], ['total_goals_1.5', best_odds2], ['total_goals_2.5', best_odds3],
                          ['total_goals_3.5', best_odds4], ['1x 2', best_odds5], ['1 x2', best_odds6],
                          ['12 x', best_odds7]]:
            if best_odds[1][0][0] is None:
                continue
            profit_percentage = event.arbitrage(best_odds[1])

            if profit_percentage > MIN_PROFIT_MARGIN:
                converted_event = convert_data(data, best_odds[1], best_odds[0], profit_percentage)
                surebets.append(converted_event)
        # TODO: refactor to here

    send_surebets_data(int(time.time()), 'football', surebets)


def handle_two_way_market(odds_response, sport):
    surebets = []
    for data in odds_response:
        event = Event(data)
        best_odds = event.find_best_odds()
        profit_percentage = event.arbitrage(best_odds)
        # if profit_percentage > 0.049:
        if profit_percentage > MIN_PROFIT_MARGIN:
            converted_event = convert_data(data, best_odds, 'h2h', profit_percentage)
            surebets.append(converted_event)

    send_surebets_data(int(time.time()), sport, surebets)


def convert_data(input_data, best_odds, market_type, profit_percentage):
    event = {
        "sport": input_data["sport_key"],
        "competition": input_data['competition'],
        "eventName": input_data["name"],
        "startTime": input_data["start_time"],
        "profitPercentage": round(profit_percentage, 2),
        "outcomes": []
    }
    # Create a dictionary to map bookie names to their odds
    bookie_odds = {}

    for bookmaker in input_data["bookmakers"]:
        for market in bookmaker["markets"]:
            if not market or market['name'] != market_type:
                continue
            for outcome in market["outcomes"]:
                bookie_name = bookmaker["title"]
                outcome_name = outcome["name"]
                outcome_odd = outcome["price"]

                if outcome_name != input_data["name"]:
                    if outcome_name not in bookie_odds:
                        bookie_odds[outcome_name] = {}
                    bookie_odds[outcome_name][bookie_name] = outcome_odd

    idx = 0
    for outcome_name, bookies in bookie_odds.items():
        outcome_data = {
            "name": outcome_name,
            "odd": best_odds[idx][2],  # Get the first bookie's odds
            "bookie": best_odds[idx][0],  # Get the first bookie's name
            "url": best_odds[idx][3],  # Provide the URL
            "otherBookies": [
                {
                    "name": bookie,
                    "odd": odd
                }
                for bookie, odd in bookies.items()
            ]
        }
        idx += 1
        event['outcomes'].append(outcome_data)

    return event


def send_surebets_data(creation_timestamp, sport, surebets):
    print(f'[{len(surebets)}] surebets found for [{sport}] at [{creation_timestamp}]')

    data = {
        'creationTimestamp': creation_timestamp,
        'sport': sport,
        'surebets': surebets
    }

    #TODO  prod should be https://arbwiz-backend.onrender.com
    base_url = os.environ['BACKEND_URL']
    url = f'{base_url}/surebets'

    requests.post(url,
                  data=json.dumps(data),
                  headers={'Content-Type': 'application/json'})

    if len(surebets) > 0:
        send_telegram_message(data)
