from data_retrievers.betano_scraper import betano_tennis_win_match_24h
from data_retrievers.betclic_http import betclic_tennis_win_match
import time

from utils import compare_strings_with_ratio

def get_data():
    aggregate_data = []
    aggregate_data = process_data_set(aggregate_data, betano_tennis_win_match_24h())
    aggregate_data = process_data_set(aggregate_data, betclic_tennis_win_match())
    data_with_at_least_two_bookmakers = list(filter(lambda event: len(event["bookmakers"]) > 1, aggregate_data['events']))
    return data_with_at_least_two_bookmakers
    
def process_data_set(aggregate_data, new_data):
    if len(aggregate_data) > 0:
        for new_event in new_data:
            was_found = False
            for event in aggregate_data['events']:
                if compare_strings_with_ratio(event['name'], new_event['name'], 0.6):

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