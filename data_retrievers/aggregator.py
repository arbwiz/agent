from data_retrievers.betano import betano_tennis_win_match_24h
from data_retrievers.betano import betano_football

from data_retrievers.betclic import betclic_tennis_win_match
from data_retrievers.betclic import betclic_football

from data_retrievers.twentytwobet import twentytwobet_tennis_win_match
from data_retrievers.twentytwobet import twentytwobet_football

from data_retrievers.esconline import esconline_tennis_win_match_24h
from data_retrievers.esconline import esconline_football

from data_retrievers.lebull import lebull_football

from data_retrievers.bwin import bwin_football

from data_retrievers.solverde import solverde_tennis

from thefuzz import process, fuzz
import time
import json
from datetime import datetime
from utils import market_types

from utils import compare_strings_with_ratio


async def get_tenis_data():
    betano = betano_tennis_win_match_24h()
    with open("output/betano_tennis.json", 'w') as outfile:
        outfile.write(json.dumps(betano, indent=4))

    betclic = betclic_tennis_win_match()
    with open("output/betclic_tennis.json", 'w') as outfile:
        outfile.write(json.dumps(betclic, indent=4))

    twentytwo = twentytwobet_tennis_win_match()
    with open("output/twentytwo_tennis.json", 'w') as outfile:
        outfile.write(json.dumps(twentytwo, indent=4))

    esconline = await esconline_tennis_win_match_24h()
    with open("output/esconline_tennis.json", 'w') as outfile:
        outfile.write(json.dumps(esconline, indent=4))

    solverde = await solverde_tennis()
    with open("output/solverde_tennis.json", 'w') as outfile:
        outfile.write(json.dumps(solverde, indent=4))

    data = aggregate_data([betclic, betano, esconline, twentytwo, solverde], 'tennis')

    with open("output/aggregated_tennis.json", 'w') as outfile:
        outfile.write(json.dumps(data, indent=4))

    return data


async def get_football_data():
    betano = betano_football()


    with open("output/betano.json", 'w') as outfile:
        outfile.write(json.dumps(betano, indent=4))

    betclic = betclic_football()

    with open("output/betclic.json", 'w') as outfile:
        outfile.write(json.dumps(betclic, indent=4))
    twentytwo = twentytwobet_football()

    with open("output/twentytwo.json", 'w') as outfile:
        outfile.write(json.dumps(twentytwo, indent=4))
    esconline = await esconline_football()

    with open("output/esconline.json", 'w') as outfile:
        outfile.write(json.dumps(esconline, indent=4))

    lebull = lebull_football()

    with open("output/lebull.json", 'w') as outfile:
        outfile.write(json.dumps(lebull, indent=4))

    bwin = bwin_football()

    with open("output/bwin.json", 'w') as outfile:
        outfile.write(json.dumps(bwin, indent=4))

    data = aggregate_data([betclic, betano, esconline, twentytwo, lebull, bwin], 'football')

    #insert_documents(data)

    with open("output/aggregated.json", 'w') as outfile:
        outfile.write(json.dumps(data, indent=4))

    return data


def aggregate_data(all_sport_data, sport_name):
    aggregate_data = []
    for sport_data in all_sport_data:
        aggregate_data = merge_data_sets(aggregate_data, sport_data, sport_name)

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
                    'title': new_event['bookmaker']
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
                    'id': time.time(),
                    'start_time': new_event['start_time'],
                    'start_time_ms': new_event['start_time_ms']
                }

                event_data['bookmakers'].append({
                    'markets': [],
                    'title': new_event['bookmaker']
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
                'id': time.time(),
                'start_time': new_event['start_time'],
                'start_time_ms': new_event['start_time_ms']
            }

            event_data['bookmakers'].append({
                'markets': [],
                'title': new_event['bookmaker']
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


def belongs_same_event(existing_events, new_event):
    event_names = [event['name'] for event in existing_events]

    event_found = process.extractOne(new_event['name'], event_names)

    idx = event_names.index(event_found[0])

    # TODO finish this


def log_aggregate_data_info(aggregate_data):
    current_time = ("\ntime:" + str(datetime.now()))
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
    last_message = ('\nsize after filters:' + str(
        len(list(filter(lambda event: len(event["bookmakers"]) > 1, aggregate_data['events'])))))

    print(
        current_time + first_message + events_with_two + events_with_tree + events_with_four + events_with_five + events_with_six + last_message)


def get_matched_event(new_event, existing_events):
    event_names = [existing_event['name'] for existing_event in existing_events]
    events_found = process.extract(new_event['name'], event_names, limit=10, scorer=fuzz.token_set_ratio)

    number_of_outcomes = len(new_event['markets'][0]['selections'])
    second_outcome_idx = 1 if number_of_outcomes == 2 else 2

    for event in events_found:
        idx = event_names.index(event[0])
        existing_event = existing_events[idx]

        if (event[1] > 70 and dates_match(new_event["start_time_ms"], existing_event["start_time_ms"])):
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