import requests
import json
import datetime

from data_retrievers.common import is_valid_tennis_event, is_valid_football_event


async def casinoportugal_tennis():
    url = "https://odds.casinoportugal.pt/redis/fixtures?take=100&type=both&countMarkets=true&lang=pt&sportId=1157"

    response = requests.get(url)

    res_dict = json.loads(response.content)

    events = []
    for event in res_dict['fixtures']:
        if event['in_play'] == 1:
            continue

        event_data = {
            'bookmaker': 'casinoportugal',
            'name': event['home_name'] + ' - ' + event['away_name'],
            'markets': [],
            'start_time': event['start_time_utc'] + 'Z',
            'start_time_ms': convert_time(event['start_time_utc'] + 'Z')
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor':
                for selection in market['selections']:
                    if selection['selection_name'] == 'Home':
                        market_data['selections'].append({
                            'name':  event['home_name'],
                            'price': float(selection['decimal'])
                        })
                    elif selection['selection_name'] == 'Away':
                        market_data['selections'].append({
                            'name':  event['away_name'],
                            'price': float(selection['decimal'])
                        })

        event_data['markets'] = [market_data]

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events


async def casinoportugal_football():
    print('casinoportugal started')
    url = "https://odds.casinoportugal.pt/redis/fixtures?take=100&type=both&countMarkets=true&lang=pt&sportId=1174"

    response = requests.get(url)

    res_dict = json.loads(response.content)

    events = []
    for event in res_dict['fixtures']:
        if event['in_play'] == 1:
            continue

        event_data = {
            'bookmaker': 'casinoportugal',
            'name': event['home_name'] + ' - ' + event['away_name'],
            'markets': [],
            'start_time': event['start_time_utc'] + 'Z',
            'start_time_ms': convert_time(event['start_time_utc'] + 'Z')
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == '1x2':
                for selection in market['selections']:
                    if selection['selection_name'] == 'Home':
                        market_data['selections'].append({
                            'name':  event['home_name'],
                            'price': float(selection['decimal'])
                        })
                    elif selection['selection_name'] == 'Away':
                        market_data['selections'].append({
                            'name':  event['away_name'],
                            'price': float(selection['decimal'])
                        })
                    else:
                        market_data['selections'].append({
                            'name': 'Empate',
                            'price': float(selection['decimal'])
                        })

        event_data['markets'] = [market_data]

        if is_valid_football_event(event_data):
            events.append(event_data)
    print('casinoportugal finished')
    return events


def convert_time(millis):
    dt = datetime.datetime.fromtimestamp(millis / 1000)
    return (dt.isoformat())


def find_market_by_id(markets, id):
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None

def convert_time(iso_format):
    dt = datetime.datetime.fromisoformat(iso_format)
    return (dt.timestamp() * 1000)