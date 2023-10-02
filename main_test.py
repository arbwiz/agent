from utils import calculate_arbitrage_3_websites
from data_retrievers.aggregator import aggregate_data
from data_retrievers.twentytwobet import twentytwobet_tennis_win_match
from data_retrievers.esconline import esconline_tennis_win_match_24h
from data_retrievers.esconline import esconline_football
from data_retrievers.betano import betano_football
from data_retrievers.betclic import betclic_football
from data_retrievers.twentytwobet import twentytwobet_football
from data_retrievers.twentytwobet import get_competition_ids
from data_retrievers.twentytwobet import get_events_from_competitions
from utils import print_properly
from utils import compare_strings_with_ratio
import difflib
import asyncio
from thefuzz import process
import json
from data_retrievers.aggregator import get_matched_event
from data_retrievers.aggregator import merge_data_sets
from data_retrievers.lebull import lebull_football
from data_retrievers.bwin import bwin_football
from model.event import calculate_arbitrage_stakes
from model.event import Event
from data_retrievers.solverde import solverde_tennis, solverde_football


async def main():
    # betano_data = [
    #     {
    #         "bookmaker": "betano",
    #         "name": "Sporting CP - Rio Ave FC",
    #         "markets": [
    #             {
    #                 "name": "h2h",
    #                 "selections": [
    #                     {"name": "Sporting CP", "price": 1.17},
    #                     {"name": "Empate", "price": 6.7},
    #                     {"name": "Rio Ave FC", "price": 14.5},
    #                 ],
    #             },
    #             {
    #                 "name": "total_goals_1.5",
    #                 "selections": [
    #                     {"name": "Over", "price": 1.17},
    #                     {"name": "Under", "price": 6.7},
    #                 ],
    #             },
    #             {
    #                 "name": "1x 2",
    #                 "selections": [
    #                     {"name": "Sporting CP ou Empate", "price": 1.17},
    #                     {"name": "Rio Ave FC", "price": 14.5},
    #                 ],
    #             },
    #         ],
    #         "start_time": "2023-09-25T20:15:00",
    #         "start_time_ms": 1695669300000,
    #     },
    #     {
    #         "bookmaker": "betano",
    #         "name": "FC Famalic\u00e3o Sub-23 - Academico Viseu Sub-23",
    #         "markets": [
    #             {
    #                 "name": "h2h",
    #                 "selections": [
    #                     {"name": "FC Famalic\u00e3o Sub-23", "price": 1.5},
    #                     {"name": "Empate", "price": 3.55},
    #                     {"name": "Academico Viseu Sub-23", "price": 4.2},
    #                 ],
    #             }
    #         ],
    #         "start_time": "2023-09-25T16:00:00",
    #         "start_time_ms": 1695654000000,
    #     },
    #     {
    #         "bookmaker": "betano",
    #         "name": "Coventry City - Huddersfield Town",
    #         "markets": [
    #             {
    #                 "name": "h2h",
    #                 "selections": [
    #                     {"name": "Coventry City", "price": 1.75},
    #                     {"name": "Empate", "price": 3.65},
    #                     {"name": "Huddersfield Town", "price": 4.3},
    #                 ],
    #             }
    #         ],
    #         "start_time": "2023-09-25T20:00:00",
    #         "start_time_ms": 1695668400000,
    #     },
    # ]
    #
    # betclic_data = [
    #     {
    #         "bookmaker": "betclic",
    #         "name": "Sporting - Rio Ave",
    #         "markets": [
    #             {
    #                 "name": "h2h",
    #                 "selections": [
    #                     {"name": "Sporting", "price": 1.18},
    #                     {"name": "Empate", "price": 6.8},
    #                     {"name": "Rio Ave", "price": 12.75},
    #                 ],
    #             },
    #             {
    #                 "name": "1 x2",
    #                 "selections": [
    #                     {"name": "Sporting CP", "price": 1.17},
    #                     {"name": "Empate ou Rio Ave FC", "price": 14.5},
    #                 ],
    #             },
    #             {
    #                 "name": "1x 2",
    #                 "selections": [
    #                     {"name": "Sporting CP ou Empate", "price": 3},
    #                     {"name": "Rio Ave FC", "price": 5},
    #                 ],
    #             },
    #         ],
    #         "start_time": "2023-09-25T19:15:00Z",
    #         "start_time_ms": 1695669300000,
    #     },
    #     {
    #         "bookmaker": "betclic",
    #         "name": "Breidablik Kopavogur - Vikingur Reykjavik",
    #         "markets": [
    #             {
    #                 "name": "h2h",
    #                 "selections": [
    #                     {"name": "Breidablik Kopavogur", "price": 2.65},
    #                     {"name": "Empate", "price": 3.23},
    #                     {"name": "Vikingur Reykjavik", "price": 1.87},
    #                 ],
    #             },
    #         ],
    #         "start_time": "2023-09-25T19:15:00Z",
    #         "start_time_ms": 1695669300000,
    #     },
    # ]
    #
    # # betano_football()
    # # await bwin_football()
    #
    # aggs = aggregate_data([betano_data, betclic_data], "football")
    #
    # events = []
    # for data in aggs:
    #     events.append(Event(data))
    #
    # arbitrage_events = []
    # for event in events:
    #     best_odds = event.find_best_odds()
    #     if event.arbitrage():
    #         arbitrage_events.append(event)

    # comps_ids = get_competition_ids()

    # events = get_events_from_competitions(comps_ids)

    solverde_task = asyncio.create_task(solverde_tennis())
    solverde = await solverde_task
    print(solverde)


def test():
    aggregated_file = open("output/aggregated_tennis.json")
    betano_file = open("output/esconline_tennis.json")

    # returns JSON object as
    # a dictionary
    aggregated = json.load(aggregated_file)
    betano_event = json.load(betano_file)[0]
    # matched_event = get_matched_event(betano_event, aggregated)

    result = merge_data_sets({"events": aggregated}, [betano_event], "football")

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
