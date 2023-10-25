import json
from datetime import datetime

import requests

from data_retrievers.common import is_valid_tennis_event, is_valid_basket_event, is_valid_football_event

all_data = {}


async def get_all_events():
    base_url = 'https://api-y-089t2gyhf4-7756.sptpub.com/api/v1/prematch/brand/1699812984232222720/pt/'
    snapshots_url = base_url + '0'
    response = requests.get(snapshots_url)

    res_dict = json.loads(response.content)

    all_items = []
    for snapshot_id in res_dict['snapshot_versions']:
        response = requests.get(base_url + str(snapshot_id))
        events = json.loads(response.content)
        all_items.extend(events['items'])

    sports = [
        {
            'name': 'tennis',
            'events': {}
        }
        ,
        {
            'name': 'football',
            'events': {}
        },
        {
            'name': 'basketball',
            'events': {}
        },
        {
            'name': 'volleyball',
            'events': {}
        }
    ]

    # Create a dictionary for quick lookup
    sports_dict = {sport['name']: sport for sport in sports}

    skip = True
    sport_name = ""

    for item in all_items:

        if item[0][1] == 'desc':
            sport_name = item[1]['sport']['slug']
            competition_name = item[1]['tournament']['slug']
            skip = False

            if sport_name in sports_dict:
                if len(item[1]['competitors']) <= 0:
                    skip = True
                    continue

                event_name = item[1]['competitors'][0]['name'] + ' - ' + item[1]['competitors'][1]['name']
                event_id = item[1]['id']

                sports_dict[sport_name]['events'][event_id] = {
                    'name': event_name,
                    'participant_a': item[1]['competitors'][0]['name'],
                    'participant_b': item[1]['competitors'][1]['name'],
                    'start_time_ms': item[1]['scheduled'],
                    'markets': [],
                    'competition': competition_name,
                }
            else:
                skip = True
                continue

        if item[0][1] == 'market' and not skip:
            event_id = item[0][0]
            if event_id in sports_dict[sport_name]['events']:
                sports_dict[sport_name]['events'][event_id]['markets'].append(item[1])

    return sports_dict


async def bettilt_football():
    global all_data
    all_data = await get_all_events()
    events = []

    for event_id, event in all_data['football']['events'].items():

        event_data = {
            'bookmaker': 'bettilt',
            'competition': event['competition'],
            'name': event['name'],
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time(event['start_time_ms'] * 1000)),
            'start_time_ms': event['start_time_ms'] * 1000,
            'url': f'https://www.bettilt363.com/pt/sportsbook?page=/event/{event_id}?isLive=false'
        }

        if len(event['markets']) >= 6:
            h2h_market_raw = event['markets'][0]
            total_goals_markets_raw = event['markets'][2]
            double_result_raw = event['markets'][5]

            if '' in h2h_market_raw:
                if '1' in h2h_market_raw[''] and '2' in h2h_market_raw[''] and '3' in h2h_market_raw['']:
                    event_data['markets'][0]['selections'].append({
                        'name': event['participant_a'],
                        'price': float(h2h_market_raw['']['1']['k'])
                    })

                    event_data['markets'][0]['selections'].append({
                        'name': 'Draw',
                        'price': float(h2h_market_raw['']['2']['k'])
                    })

                    event_data['markets'][0]['selections'].append({
                        'name': event['participant_b'],
                        'price': float(h2h_market_raw['']['3']['k'])
                    })

            double_results_markets = get_double_result_markets(double_result_raw, event_data['markets'][0])
            event_data['markets'].extend(double_results_markets)

            total_goals_markets_raw = get_total_goals_markets(total_goals_markets_raw)
            event_data['markets'].extend(total_goals_markets_raw)

        if is_valid_football_event(event_data):
            events.append(event_data)
    return events


async def bettilt_tennis():
    events = []
    for event_id, event in all_data['tennis']['events'].items():

        event_data = {
            'bookmaker': 'bettilt',
            'competition': event['competition'],
            'name': event['name'],
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time(event['start_time_ms'] * 1000)),
            'start_time_ms': event['start_time_ms'] * 1000,
            'url': f'https://www.bettilt363.com/pt/sportsbook?page=/event/{event_id}?isLive=false'
        }

        for market in event['markets']:
            if '' in market:
                event_data['markets'][0]['selections'].append({
                    'name': event['participant_a'],
                    'price': float(market['']['4']['k'])
                })

                event_data['markets'][0]['selections'].append({
                    'name': event['participant_b'],
                    'price': float(market['']['5']['k'])
                })

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events

async def bettilt_volley():
    events = []
    for event_id, event in all_data['volleyball']['events'].items():

        event_data = {
            'bookmaker': 'bettilt',
            'competition': event['competition'],
            'name': event['name'],
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time(event['start_time_ms'] * 1000)),
            'start_time_ms': event['start_time_ms'] * 1000,
            'url': f'https://www.bettilt363.com/pt/sportsbook?page=/event/{event_id}?isLive=false'
        }

        for market in event['markets']:
            if '' in market:
                event_data['markets'][0]['selections'].append({
                    'name': event['participant_a'],
                    'price': float(market['']['4']['k'])
                })

                event_data['markets'][0]['selections'].append({
                    'name': event['participant_b'],
                    'price': float(market['']['5']['k'])
                })

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events

async def bettilt_basket():
    events = []
    for event_id, event in all_data['basketball']['events'].items():

        event_data = {
            'bookmaker': 'bettilt',
            'competition': event['competition'],
            'name': event['name'],
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time(event['start_time_ms'] * 1000)),
            'start_time_ms': event['start_time_ms'] * 1000,
            'url': f'https://www.bettilt363.com/pt/sportsbook?page=/event/{event_id}?isLive=false'
        }

        for market in event['markets']:
            if '' in market and ('4' in market[''] and '5' in market['']):
                event_data['markets'][0]['selections'].append({
                    'name': event['participant_a'],
                    'price': float(market['']['4']['k'])
                })

                event_data['markets'][0]['selections'].append({
                    'name': event['participant_b'],
                    'price': float(market['']['5']['k'])
                })

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events


def convert_time(millis):
    dt = datetime.fromtimestamp(millis / 1000)
    return (dt.isoformat())


def find_market_by_id(markets, id):
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None


def get_double_result_markets(double_result_market, h2h_market):
    if '' not in double_result_market:
        return []

    if '9' not in double_result_market[''] or '10' not in double_result_market[''] or '11' not in double_result_market[
        '']:
        return []

    market = {
        'name': '1x 2',
        'selections': [
            {
                'name': '1x',
                'price': float(double_result_market['']['9']['k'])
            },
            {
                'name': '2',
                'price': h2h_market['selections'][2]['price']
            }
        ]
    }

    market2 = {
        'name': '1 x2',
        'selections': [
            {
                'name': '1',
                'price': h2h_market['selections'][0]['price']
            },
            {
                'name': 'x2',
                'price': float(double_result_market['']['11']['k'])
            }
        ]
    }

    market3 = {
        'name': '12 x',
        'selections': [
            {
                'name': '12',
                'price': float(double_result_market['']['10']['k'])
            },
            {
                'name': 'x',
                'price': h2h_market['selections'][1]['price']
            }
        ]
    }

    if len(market['selections']) != 2 or len(market2['selections']) != 2 or len(market3['selections']) != 2:
        return None

    return [market, market2, market3]


def get_total_goals_markets(total_goals_markets_raw):
    markets = []
    if 'total=1.5' in total_goals_markets_raw:
        markets.append(get_market_with_handicap(total_goals_markets_raw, '1.5'))
    if 'total=2.5' in total_goals_markets_raw:
        markets.append(get_market_with_handicap(total_goals_markets_raw, '2.5'))
    if 'total=3.5' in total_goals_markets_raw:
        markets.append(get_market_with_handicap(total_goals_markets_raw, '3.5'))

    return markets


def get_market_with_handicap(markets_raw, handicap):
    over = markets_raw[f'total={handicap}']['12']['k']
    under = markets_raw[f'total={handicap}']['13']['k']
    return {
        'name': f'total_goals_{handicap}',
        'selections': [
            {
                'name': f'Over {handicap}',
                'price': float(over)
            },
            {
                'name': f'Under {handicap}',
                'price': float(under)
            }
        ]
    }
