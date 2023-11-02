from data_retrievers.betano import betano_tennis_win_match_24h, betano_basket, betano_volley, betano_american_football
from data_retrievers.betano import betano_football

from data_retrievers.betclic import betclic_tennis_win_match, betclic_basket, betclic_volley, betclic_american_football
from data_retrievers.betclic import betclic_football
from data_retrievers.betseven import betseven_tennis, betseven_basket, betseven_football, betseven_american_football
from data_retrievers.bettilt import bettilt_tennis, bettilt_basket, bettilt_football, bettilt_volley
from data_retrievers.casinoportugal import casinoportugal_tennis, casinoportugal_football
from data_retrievers.placard import placard_tennis, placard_football, placard_basket

from data_retrievers.twentytwobet import twentytwobet_tennis_win_match, twentytwobet_basket, twentytwobet_volley, \
    twentytwobet_american_football
from data_retrievers.twentytwobet import twentytwobet_football

from data_retrievers.esconline import esconline_tennis_win_match_24h, esconline_basket
from data_retrievers.esconline import esconline_football

from data_retrievers.lebull import lebull_football, lebull_tennis, lebull_basket

from data_retrievers.bwin import bwin_football, bwin_tennis, bwin_basket

from data_retrievers.solverde import solverde_tennis, solverde_football, solverde_basket

from thefuzz import process, fuzz
import time
import json
from datetime import datetime
from utils import market_types

import asyncio

from utils import compare_strings_with_ratio


async def get_american_football_data():
    twentytwo_t = asyncio.create_task(twentytwobet_american_football())
    betano_t = asyncio.create_task(betano_american_football())
    betclic_t = asyncio.create_task(betclic_american_football())
    betseven_t = asyncio.create_task(betseven_american_football())

    bookmakers = []

    for func in [["twentytwo", twentytwo_t],
                 ["betano", betano_t],
                 ["betclic", betclic_t],
                 ["betseven", betseven_t]]:
        try:
            result = await func[1]
        except Exception as e:
            print(f"Error at volley for provider: [{func[0]}] with exception: [{e}]")
            result = []
        bookmakers.append(result)

    data = aggregate_data(bookmakers, 'american_football')

    await generate_output_files(bookmakers, data, 'american_football')

    return data

async def get_volley_data():
    twentytwo_t = asyncio.create_task(twentytwobet_volley())
    betano_t = asyncio.create_task(betano_volley())
    betclic_t = asyncio.create_task(betclic_volley())
    bettilt_t = asyncio.create_task(bettilt_volley())

    bookmakers = []

    for func in [["twentytwo", twentytwo_t],
                 ["betano", betano_t],
                 ["betclic", betclic_t],
                 ["bettilt", bettilt_t]]:
        try:
            result = await func[1]
        except Exception as e:
            print(f"Error at volley for provider: [{func[0]}] with exception: [{e}]")
            result = []
        bookmakers.append(result)

    data = aggregate_data(bookmakers, 'volleyball')

    await generate_output_files(bookmakers, data, 'volleyball')

    return data

async def get_tennis_data():
    solverde_t = asyncio.create_task(solverde_tennis())
    placard_t = asyncio.create_task(placard_tennis())
    twentytwo_t = asyncio.create_task(twentytwobet_tennis_win_match())
    esconline_t = asyncio.create_task(esconline_tennis_win_match_24h())
    betano_t = asyncio.create_task(betano_tennis_win_match_24h())
    betclic_t = asyncio.create_task(betclic_tennis_win_match())
    lebull_t = asyncio.create_task(lebull_tennis())
    bwin_t = asyncio.create_task(bwin_tennis())
    casinoportugal_t = asyncio.create_task(casinoportugal_tennis())
    betseven_t = asyncio.create_task(betseven_tennis())
    bettilt_t = asyncio.create_task(bettilt_tennis())

    bookmakers = []

    for func in [["solverde", solverde_t],
                 ["placard", placard_t],
                 ["twentytwo", twentytwo_t],
                 ["esconline", esconline_t],
                 ["betano", betano_t],
                 ["betclic", betclic_t],
                 ["lebull", lebull_t],
                 ["bwin", bwin_t],
                 ["casinoportugal", casinoportugal_t],
                 ["betseven", betseven_t],
                 ["bettilt", bettilt_t]]:
        try:
            result = await func[1]
        except Exception as e:
            print(f"Error at tennis for provider: [{func[0]}] with exception: [{e}]")
            result = []
        bookmakers.append(result)

    data = aggregate_data(bookmakers, 'tennis')

    await generate_output_files(bookmakers, data, 'tennis')

    return data


async def get_basket_data():
    solverde_t = asyncio.create_task(solverde_basket())
    placard_t = asyncio.create_task(placard_basket())
    twentytwo_t = asyncio.create_task(twentytwobet_basket())
    esconline_t = asyncio.create_task(esconline_basket())
    betano_t = asyncio.create_task(betano_basket())
    betclic_t = asyncio.create_task(betclic_basket())
    lebull_t = asyncio.create_task(lebull_basket())
    bwin_t = asyncio.create_task(bwin_basket())
    # not supported yet due to default winner market having draw option
    # casinoportugal_t = asyncio.create_task(casinoportugal_basket())
    betseven_t = asyncio.create_task(betseven_basket())
    bettilt_t = asyncio.create_task(bettilt_basket())

    bookmakers = []

    for func in [["solverde", solverde_t],
                 ["twentytwo", twentytwo_t],
                 ["esconline", esconline_t],
                 ["betano", betano_t],
                 ["betclic", betclic_t],
                 ["lebull", lebull_t],
                 ["bwin", bwin_t],
                 ["placard", placard_t],
                 ["betseven", betseven_t],
                 ["bettilt", bettilt_t]]:
        try:
            result = await func[1]
        except Exception as e:
            print(f"Error at basket for provider: [{func[0]}] with exception: [{e}]")
            result = []
        bookmakers.append(result)

    data = aggregate_data(bookmakers, 'basket')

    await generate_output_files(bookmakers, data, 'basket')
    return data


async def get_football_data():
    solverde_t = asyncio.create_task(solverde_football())
    twentytwo_t = asyncio.create_task(twentytwobet_football())
    esconline_t = asyncio.create_task(esconline_football())
    betano_t = asyncio.create_task(betano_football())
    betclic_t = asyncio.create_task(betclic_football())
    lebull_t = asyncio.create_task(lebull_football())
    bwin_t = asyncio.create_task(bwin_football())
    placard_t = asyncio.create_task(placard_football())
    casinoportugal_t = asyncio.create_task(casinoportugal_football())
    betseven_t = asyncio.create_task(betseven_football())
    bettilt_t = asyncio.create_task(bettilt_football())

    bookmakers = []

    for func in [["solverde", solverde_t],
                 ["placard", placard_t],
                 ["twentytwo", twentytwo_t],
                 ["esconline", esconline_t],
                 ["betano", betano_t],
                 ["betclic", betclic_t],
                 ["lebull", lebull_t],
                 ["bwin", bwin_t],
                 ["casinoportugal", casinoportugal_t],
                 ["betseven", betseven_t],
                 ["bettilt", bettilt_t]]:

        try:
            result = await func[1]
        except Exception as e:
            print(f"Error at football for provider: [{func[0]}] with exception: [{e}]")
            result = []
        bookmakers.append(result)

    data = aggregate_data(bookmakers, 'football')

    await generate_output_files(bookmakers, data, 'football')

    return data


def aggregate_data(all_sport_data, sport_name):
    aggregate_data = []
    for sport_data in all_sport_data:
        aggregate_data = merge_data_sets(aggregate_data, sport_data, sport_name)

    print('\n======' + sport_name + '=======')
    log_aggregate_data_info(aggregate_data)

    data_with_at_least_two_bookmakers = list(
        filter(lambda event: len(event["bookmakers"]) > 1, aggregate_data['events']))

    return data_with_at_least_two_bookmakers


def merge_data_sets(aggregate_data, new_data, sport_name):
    if len(aggregate_data) > 0:
        for new_event in new_data:

            matched_event = get_matched_event(new_event, aggregate_data['events'])

            if matched_event is not None:
                event = matched_event

                if has_bookmaker_title(event, new_event['bookmaker']):
                    continue

                event['bookmakers'].append({
                    'markets': [],
                    'title': new_event['bookmaker'],
                    'url': new_event['url']
                })

                markets = []

                for index, market_type in enumerate(market_types):
                    market_found = get_market(new_event['markets'], 'name', market_type)
                    if market_found is None:
                        markets.insert(index, [])
                    else:
                        outcomes = []
                        for i, selection in enumerate(market_found['selections']):
                            existing_markets = event['bookmakers'][0]['markets'][index]
                            outcomes.append({
                                # normalize outcome name, keep the first bookmaker names
                                'name': selection['name'] if len(existing_markets) == 0 else
                                event['bookmakers'][0]['markets'][index]['outcomes'][i]['name'],
                                'original_name': selection['name'],
                                'price': selection['price']
                            })
                        market_data = {
                            'outcomes': outcomes,
                            'name': market_type
                        }

                        markets.insert(index, market_data)

                event['bookmakers'][len(event['bookmakers']) - 1]['markets'] = markets

            else:
                event_data = {
                    'name': new_event['name'],
                    'bookmakers': [],
                    'sport_key': sport_name,
                    'competition': new_event['competition'],
                    'id': time.time(),
                    'start_time': new_event['start_time'],
                    'start_time_ms': new_event['start_time_ms']
                }

                event_data['bookmakers'].append({
                    'markets': [],
                    'title': new_event['bookmaker'],
                    'url': new_event['url']
                })

                markets = []

                for index, market_type in enumerate(market_types):
                    market_found = get_market(new_event['markets'], 'name', market_type)
                    if market_found is None:
                        markets.insert(index, [])
                    else:
                        outcomes = []
                        for selection in market_found['selections']:
                            outcomes.append({
                                'name': selection['name'],
                                'original_name': selection['name'],
                                'price': selection['price']
                            })
                        market_data = {
                            'outcomes': outcomes,
                            'name': market_type
                        }

                        markets.insert(index, market_data)

                event_data['bookmakers'][len(event_data['bookmakers']) - 1]['markets'] = markets

                aggregate_data['events'].append(event_data)
    else:
        aggregate_data = {
            'events': []
        }

        for new_event in new_data:
            event_data = {
                'name': new_event['name'],
                'bookmakers': [],
                'sport_key': sport_name,
                'competition': new_event['competition'],
                'id': time.time(),
                'start_time': new_event['start_time'],
                'start_time_ms': new_event['start_time_ms']
            }

            event_data['bookmakers'].append({
                'markets': [],
                'title': new_event['bookmaker'],
                'url': new_event['url']
            })

            markets = []

            for index, market_type in enumerate(market_types):
                market_found = get_market(new_event['markets'], 'name', market_type)
                if market_found is None:
                    markets.insert(index, [])
                else:
                    outcomes = []
                    for selection in market_found['selections']:
                        outcomes.append({
                            'name': selection['name'],
                            'original_name': selection['name'],
                            'price': selection['price']
                        })
                    market_data = {
                        'outcomes': outcomes,
                        'name': market_type
                    }

                    markets.insert(index, market_data)

            event_data['bookmakers'][len(event_data['bookmakers']) - 1]['markets'] = markets

            aggregate_data['events'].append(event_data)

    return aggregate_data


def contains_event_name(events, name):
    return compare_strings_with_ratio(events['name'], name, 0.6)

async def generate_output_files(bookmakers, aggregated, sport_type):

    await write_output_file(f"aggregated_{sport_type}", aggregated)
    for bookmaker in bookmakers:
        if len(bookmaker) > 0:
            await write_output_file(f"{bookmaker[0]['bookmaker']}_{sport_type}", bookmaker)


async def write_output_file(file_name, file_data):
    with open("output/" + file_name + ".json", 'w') as outfile:
        outfile.write(json.dumps(file_data, indent=4))
    outfile.close()

def log_aggregate_data_info(aggregate_data):
    current_time = ("time:" + str(datetime.now()))
    first_message = ('\nsize before filters:' + str(len(aggregate_data['events'])))
    events_with_two = ('\nevents with two bookmakers:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) == 2, aggregate_data['events'])))))
    events_with_tree = ('\nevents with three bookmakers:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) == 3, aggregate_data['events'])))))
    events_with_four = ('\nevents with four bookmakers:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) == 4, aggregate_data['events'])))))
    events_with_five = ('\nevents with five bookmakers:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) == 5, aggregate_data['events'])))))
    events_with_six = ('\nevents with six bookmakers:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) == 6, aggregate_data['events'])))))
    events_with_seven = ('\nevents with seven bookmakers:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) == 7, aggregate_data['events'])))))
    events_with_eight = ('\nevents with eight bookmakers:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) == 8, aggregate_data['events'])))))
    events_with_nine = ('\nevents with nine bookmakers:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) == 9, aggregate_data['events'])))))
    last_message = ('\nsize after filters:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) > 1, aggregate_data['events'])))))

    print(
        current_time + first_message + events_with_two + events_with_tree + events_with_four + events_with_five + events_with_six + events_with_seven,
        events_with_eight, events_with_nine + last_message)


def get_matched_event(new_event, existing_events):
    event_names = [existing_event['name'] for existing_event in existing_events]
    events_found = process.extract(new_event['name'], event_names, limit=10, scorer=fuzz.token_set_ratio)

    number_of_outcomes = len(new_event['markets'][0]['selections'])
    second_outcome_idx = 1 if number_of_outcomes == 2 else 2

    for event in events_found:
        idx = event_names.index(event[0])
        existing_event = existing_events[idx]

        if 'outcomes' not in existing_event["bookmakers"][0]['markets'][0]:
            continue

        if event[1] > 70 and dates_match(new_event["start_time_ms"], existing_event["start_time_ms"]):
            if (
                    compare_strings_with_ratio(new_event['markets'][0]['selections'][0]['name'],
                                               existing_event["bookmakers"][0]['markets'][0]['outcomes'][0]['name'],
                                               0.6)
                    and
                    compare_strings_with_ratio(new_event['markets'][0]['selections'][second_outcome_idx]['name'],
                                               existing_event["bookmakers"][0]['markets'][0]['outcomes'][
                                                   second_outcome_idx]['name'], 0.6)
            ):
                return existing_event
    return None


def dates_match(date1, date2):
    dif = abs(date1 - date2)
    # if diff is less than 1 hour, consider a match
    return dif <= 3600000


def get_market(markets, field_name, field_value):
    if len(markets) == 0 or markets is None:
        return None
    return next((obj for obj in markets if obj is not None and obj.get(field_name) == field_value), None)


def has_bookmaker_title(event, bookmaker_title):
    """Checks if the given event has a bookmaker with the given title.

    Args:
      event: A dictionary representing an event.
      bookmaker_title: The title of the bookmaker to check for.

    Returns:
      True if the event has a bookmaker with the given title, False otherwise.
    """

    for bookmaker in event["bookmakers"]:
        if bookmaker["title"] == bookmaker_title:
            return True
    return False
