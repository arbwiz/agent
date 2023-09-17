from data_retrievers.betano import betano_tennis_win_match_24h
from data_retrievers.betano import betano_football

from data_retrievers.betclic import betclic_tennis_win_match
from data_retrievers.betclic import betclic_football

from data_retrievers.twentytwobet import twentytwobet_tennis_win_match
from data_retrievers.twentytwobet import twentytwobet_football

from data_retrievers.esconline import esconline_tennis_win_match_24h
from data_retrievers.esconline import esconline_football

import time

from utils import compare_strings_with_ratio
from notifications.telegram import send_telegram_message



async def get_tenis_data():
    aggregate_data = []
    aggregate_data = process_data_set(aggregate_data, betano_tennis_win_match_24h())
    aggregate_data = process_data_set(aggregate_data, betclic_tennis_win_match())
    aggregate_data = process_data_set(aggregate_data, twentytwobet_tennis_win_match())
    aggregate_data = process_data_set(aggregate_data, await esconline_tennis_win_match_24h())
    
    print('size before filter:' + str(len(aggregate_data['events'])))
    data_with_at_least_two_bookmakers = list(filter(lambda event: len(event["bookmakers"]) > 1, aggregate_data['events']))
    print('size after filter:' + str(len(data_with_at_least_two_bookmakers)))
    return data_with_at_least_two_bookmakers
    
async def get_football_data():
    aggregate_data = []
    aggregate_data = process_data_set(aggregate_data, betano_football())
    aggregate_data = process_data_set(aggregate_data, betclic_football())
    aggregate_data = process_data_set(aggregate_data, twentytwobet_football())
    aggregate_data = process_data_set(aggregate_data, await esconline_football())
    
    first_message = ('\ntotal events' + str(len(aggregate_data['events'])))
    data_with_at_least_two_bookmakers = list(filter(lambda event: len(event["bookmakers"]) > 1, aggregate_data['events']))
    events_with_two = ('\nevents with two bookmakers:' + str(len(list(filter(lambda event: len(event["bookmakers"]) == 2, aggregate_data['events'])))))
    events_with_tree = ('\nevents with three bookmakers:' + str(len(list(filter(lambda event: len(event["bookmakers"]) == 3, aggregate_data['events'])))))
    events_with_four = ('\nevents with four bookmakers:' + str(len(list(filter(lambda event: len(event["bookmakers"]) == 4, aggregate_data['events'])))))
    last_message = ('\nsize after filter:' + str(len(data_with_at_least_two_bookmakers)))
    
    send_telegram_message(first_message + events_with_two + events_with_tree + events_with_four + last_message)
    print(first_message + events_with_two + events_with_tree + events_with_four + last_message)
    return data_with_at_least_two_bookmakers

def process_data_set(aggregate_data, new_data):
    if len(aggregate_data) > 0:
        for new_event in new_data:
            was_found = False
            for event in aggregate_data['events']:
                if compare_strings_with_ratio(event['name'], new_event['name'], 0.80):

                    if any(bookmaker['title'] == new_event['bookmaker'] for bookmaker in event['bookmakers']):
                        was_found = True
                        break

                    event['bookmakers'].append({
                        'markets':[],
                        'title': new_event['bookmaker']
                    })
                                    
                    event['bookmakers'][len(event['bookmakers']) - 1]['markets'].append({
                        'outcomes': [],
                        'name': 'h2h'
                    })
                    for selection in new_event['selections']: 
                        event['bookmakers'][len(event['bookmakers']) - 1]['markets'][0]['outcomes'].append({
                            'name': selection['name'],
                            'price': selection['price']
                        })
                    was_found = True
                    break
            if not was_found:
                event_data = {
                    'name': new_event['name'],
                    'bookmakers' : [],
                    'sport_key': "tennis",
                    'id': time.time
                }
                
                event_data['bookmakers'].append({
                    'markets':[],
                    'title': new_event['bookmaker']
                })

                #TODO: should also check if new selections name match existent (at least last event with new) so that there are less errors on
                # matched events
                event_data['bookmakers'][len(event_data['bookmakers']) - 1]['markets'].append({
                    'outcomes': [],
                    'name': 'h2h'
                })

                for selection in new_event['selections']: 
                    event_data['bookmakers'][len(event_data['bookmakers']) - 1]['markets'][0]['outcomes'].append({
                        'name': selection['name'],
                        'price': selection['price']
                })

                aggregate_data['events'].append(event_data)
    else:
        aggregate_data = {
            'events': []
        }

        for new_event in new_data:
            event_data = {
                    'name': new_event['name'],
                    'bookmakers' : [],
                    'sport_key': "tennis",
                    'id': time.time
                }
            
            event_data['bookmakers'].append({
                'markets':[],
                'title': new_event['bookmaker']
            })

            event_data['bookmakers'][len(event_data['bookmakers']) - 1]['markets'].append({
                'outcomes': [],
                'name': 'h2h'
            })

            for selection in new_event['selections']: 
                event_data['bookmakers'][len(event_data['bookmakers']) - 1]['markets'][0]['outcomes'].append({
                    'name': selection['name'],
                    'price': selection['price']
                })

            aggregate_data['events'].append(event_data)
        
    return aggregate_data

def contains_event_name(events, name):
    return compare_strings_with_ratio(events['name'], name, 0.6)