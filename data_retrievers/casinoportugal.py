import requests
import json
import datetime

from data_retrievers.common import is_valid_tennis_event, is_valid_football_event, is_valid_basket_event


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
            'competition': event['region_name'] + ' - ' + event['comp_name'],
            'name': event['home_name'] + ' - ' + event['away_name'],
            'markets': [],
            'start_time': event['start_time_utc'] + 'Z',
            'start_time_ms': convert_time(event['start_time_utc'] + 'Z'),
            'url': 'https://www.casinoportugal.pt/desportos/mercados/' + str(event['id'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor' and market['trading_status'] != 'Suspended':
                for selection in market['selections']:
                    if selection['selection_name'] == 'Home':
                        market_data['selections'].append({
                            'name': event['home_name'],
                            'price': float(selection['decimal'])
                        })
                    elif selection['selection_name'] == 'Away':
                        market_data['selections'].append({
                            'name': event['away_name'],
                            'price': float(selection['decimal'])
                        })

        event_data['markets'] = [market_data]

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events


async def casinoportugal_basket():
    url = "https://odds.casinoportugal.pt/redis/fixtures?take=100&type=both&countMarkets=true&lang=pt&sportId=1282"

    response = requests.get(url)

    res_dict = json.loads(response.content)

    events = []
    for event in res_dict['fixtures']:
        if event['in_play'] == 1:
            continue

        event_data = {
            'bookmaker': 'casinoportugal',
            'competition': event['region_name'] + ' - ' + event['comp_name'],
            'name': event['home_name'] + ' - ' + event['away_name'],
            'markets': [],
            'start_time': event['start_time_utc'] + 'Z',
            'start_time_ms': convert_time(event['start_time_utc'] + 'Z'),
            'url': 'https://www.casinoportugal.pt/desportos/mercados/' + str(event['id'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == '1x2' and market['trading_status'] != 'Suspended':
                for selection in market['selections']:
                    if selection['selection_name'] == 'Home':
                        market_data['selections'].append({
                            'name': event['home_name'],
                            'price': float(selection['decimal'])
                        })
                    elif selection['selection_name'] == 'Away':
                        market_data['selections'].append({
                            'name': event['away_name'],
                            'price': float(selection['decimal'])
                        })
                    else:
                        continue

        event_data['markets'] = [market_data]

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events


async def casinoportugal_football():
    url = "https://odds.casinoportugal.pt/redis/fixtures?take=100&type=both&countMarkets=true&lang=pt&sportId=1174"

    response = requests.get(url)

    res_dict = json.loads(response.content)

    events = []
    for event in res_dict['fixtures']:
        if event['in_play'] == 1:
            continue

        event_data = {
            'bookmaker': 'casinoportugal',
            'competition': event['region_name'] + ' - ' + event['comp_name'],
            'name': event['home_name'] + ' - ' + event['away_name'],
            'markets': [],
            'start_time': event['start_time_utc'] + 'Z',
            'start_time_ms': convert_time(event['start_time_utc'] + 'Z'),
            'url': 'https://www.casinoportugal.pt/desportos/mercados/' + str(event['id'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == '1x2' and market['trading_status'] != 'Suspended':
                for selection in market['selections']:
                    if selection['selection_name'] == 'Home':
                        market_data['selections'].append({
                            'name': event['home_name'],
                            'price': float(selection['decimal'])
                        })
                    elif selection['selection_name'] == 'Away':
                        market_data['selections'].append({
                            'name': event['away_name'],
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
    return events


def convert_time(millis):
    dt = datetime.datetime.fromtimestamp(millis / 1000)
    return dt.isoformat()


def find_market_by_id(markets, id):
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None


def convert_time(iso_format):
    dt = datetime.datetime.fromisoformat(iso_format)
    return dt.timestamp() * 1000
