from data_retrievers.betseven import betseven_tennis, betseven_basket, betseven_football, betseven_american_football
from data_retrievers.bettilt import get_all_events, bettilt_tennis, bettilt_football, bettilt_volley
from data_retrievers.casinoportugal import casinoportugal_football, casinoportugal_tennis, casinoportugal_basket
from data_retrievers.placard import placard_football, placard_basket
from data_retrievers.placard import placard_tennis
from utils import calculate_arbitrage_3_websites
from data_retrievers.twentytwobet import twentytwobet_tennis_win_match, twentytwobet_basket, twentytwobet_volley, \
    twentytwobet_american_football
from data_retrievers.esconline import esconline_tennis_win_match_24h, esconline_basket
from data_retrievers.esconline import esconline_football
from data_retrievers.betano import betano_football, betano_basket, betano_volley, betano_american_football
from data_retrievers.betclic import betclic_football, betclic_basket, betclic_volley, betclic_american_football
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
from data_retrievers.lebull import lebull_football, lebull_basket
from data_retrievers.bwin import bwin_football, bwin_basket
from model.event import calculate_arbitrage_stakes
from model.event import Event
from data_retrievers.solverde import solverde_tennis, solverde_football, solverde_basket


async def main():
    await test()


async def test():
    # aggregated_file = open("output/aggregated_tennis.json")
    # betano_file = open("output/esconline_tennis.json")

    # returns JSON object as
    # a dictionary
    # aggregated = json.load(aggregated_file)
    # betano_event = json.load(betano_file)[0]
    # matched_event = get_matched_event(betano_event, aggregated)

    # result = merge_data_sets({"events": aggregated}, [betano_event], "football")

    # print(result)

    data = await betseven_basket()
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
