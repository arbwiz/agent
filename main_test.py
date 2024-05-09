import time
import traceback
import re

import unidecode

from data_retrievers.betseven import betseven_tennis, betseven_basket, betseven_football, betseven_american_football
from data_retrievers.bettilt import get_all_events, bettilt_tennis, bettilt_football, bettilt_volley
from data_retrievers.betway import betway_tennis, convert_time_plus2_ms, convert_time_from_plus2_to_z, betway_basket
from data_retrievers.casinoportugal import casinoportugal_football, casinoportugal_tennis, casinoportugal_basket
from data_retrievers.leonbet import leonbet_tennis
from data_retrievers.placard import placard_football, placard_basket
from data_retrievers.placard import placard_tennis
from logic.main import run
from utils import calculate_arbitrage_3_websites
from data_retrievers.twentytwobet import twentytwobet_tennis_win_match, twentytwobet_basket, twentytwobet_volley, \
    twentytwobet_american_football
from data_retrievers.esconline import esconline_tennis_win_match_24h, esconline_basket
from data_retrievers.esconline import esconline_football
from data_retrievers.betano import betano_football, betano_basket, betano_volley, betano_american_football, betano_tennis
from data_retrievers.betclic import betclic_football, betclic_basket, betclic_volley, betclic_american_football, \
    betclic_tennis
from data_retrievers.twentytwobet import twentytwobet_football
from data_retrievers.twentytwobet import get_competition_ids
from data_retrievers.twentytwobet import get_events_from_competitions
from utils import print_properly
from utils import compare_strings_with_ratio
import difflib
import asyncio
from thefuzz import process, fuzz
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

    # model = GPT4All("mistral-7b-openorca.Q4_0.gguf", device="gpu")
    # model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", device="gpu")
    # system_template = ('You are a sport events analyst that knows all the data regarding team, competitions and event names from all existing sports in all countries.')
    # prompt_template = 'USER: {0}\nASSISTANT:'
    #
    # with model.chat_session(system_template, prompt_template):
    #     start_time = time.time()
    #     response1 = model.generate('Event 1:\nLeague: TFF 1. Lig\nTeams: Boluspor vs Sakaryaspor\n\nEvent 2:\nLeague: 2-lig\nTeams: Inegolspor vs Usakspor\n Does this events represent the same match? Answer True or False')
    #
    #     end_time = time.time()
    #     time_taken = end_time - start_time
    #     print(response1)

    # result = process.extract(sanitize_text("Orl. Loiret-Basquetebol"),
    #                          [sanitize_text("Orle\u00e3es Loiret Basquetebol")], limit=10,
    #                          scorer=fuzz.token_set_ratio)

    result = await betway_tennis()
    print(result)



if __name__ == "__main__":
    asyncio.run(main())


