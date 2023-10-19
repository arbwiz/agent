from model.event import Event
from data_retrievers.aggregator import get_tennis_data, get_basket_data, get_volley_data
from data_retrievers.aggregator import get_football_data


async def run(sport):
    match sport:
        case 'football':
            odds_response = await get_football_data()
            handle_football(odds_response)
        case 'tennis':
            odds_response = await get_tennis_data()
            handle_tennis(odds_response)
        case 'basket':
            odds_response = await get_basket_data()
            handle_tennis(odds_response)
        case 'volleyball':
            odds_response = await get_volley_data()
            handle_tennis(odds_response)
        case _:
            odds_response = await get_tennis_data()
            handle_tennis(odds_response)


def handle_football(odds_response):
    for data in odds_response:
        event = (Event(data))

        # check why there are errors on logs
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

        event.arbitrage(best_odds1)
        event.arbitrage(best_odds2)
        event.arbitrage(best_odds3)
        event.arbitrage(best_odds4)
        event.arbitrage(best_odds5)
        event.arbitrage(best_odds6)
        event.arbitrage(best_odds7)


def handle_tennis(odds_response):
    for data in odds_response:
        event = Event(data)
        best_odds = event.find_best_odds()
        event.arbitrage(best_odds)
