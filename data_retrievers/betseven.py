import json
from datetime import datetime

import requests

from data_retrievers.common import is_valid_tennis_event, is_valid_basket_event, is_valid_football_event


async def betseven_tennis():
    result_events = await get_events('tennis')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': 'betseven',
            'name': event['participants']['home']['name'] + ' - ' + event['participants']['away']['name'],
            'markets': [],
            'start_time': event['startTime'],
            'start_time_ms': convert_time(event['startTime'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor':
                for selection in market['odds']:
                    market_data['selections'].append({
                        'name': selection['name'],
                        'price': float(selection['value'])
                    })

        event_data['markets'] = [market_data]

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events


async def betseven_basket():
    result_events = await get_events('basket')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': 'betseven',
            'name': event['participants']['home']['name'] + ' - ' + event['participants']['away']['name'],
            'markets': [],
            'start_time': event['startTime'],
            'start_time_ms': convert_time(event['startTime'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor (incluindo prorrogação)':
                for selection in market['odds']:
                    market_data['selections'].append({
                        'name': selection['name'],
                        'price': float(selection['value'])
                    })

        event_data['markets'] = [market_data]

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events


async def betseven_football():
    result_events = await get_events('football')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': 'betseven',
            'name': event['participants']['home']['name'] + ' - ' + event['participants']['away']['name'],
            'markets': [],
            'start_time': event['startTime'],
            'start_time_ms': convert_time(event['startTime'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor':
                for selection in market['odds']:

                    for odd in market['odds']:
                        if odd['type'] == 1:
                            market_data['selections'].insert(0, {
                                'name': selection['name'],
                                'price': float(selection['value'])
                            })
                        elif odd['type'] == 2:
                            market_data['selections'].insert(1, {
                                'name': selection['name'],
                                'price': float(selection['value'])
                            })
                        elif odd['type'] == 3:
                            market_data['selections'].insert(2, {
                                'name': selection['name'],
                                'price': float(selection['value'])
                            })

        event_data['markets'] = [market_data]

        dr_markets = get_double_result_markets(event, market_data)
        ou_markets = get_total_goals_market(event)

        if dr_markets is not None:
            event_data['markets'].extend(dr_markets)
        if ou_markets is not None:
            event_data['markets'].extend(ou_markets)

        if is_valid_football_event(event_data):
            events.append(event_data)
    return events


async def get_events(sport_arg):
    sport_id = 1
    sport_name = 'Football'

    if sport_arg == 'football':
        sport_id = 1
        sport_name = 'Football'
        market_type_ids = "&marketTypeIds[]=1&marketTypeIds[]=10&marketTypeIds[]=18"
    elif sport_arg == 'tennis':
        sport_id = 5
        sport_name = 'Tennis'
        market_type_ids = "&marketTypeIds[]=186"
    elif sport_arg == 'basket':
        sport_id = 2
        sport_name = 'Basketball'
        market_type_ids = "&marketTypeIds[]=219"

    comps_url = (
        f"https://www.bet7.com/iapi/sportsbook/v2/sports/{sport_id}/tournaments?timespan=24{market_type_ids}").format(
        sport_id=sport_id, market_type_ids=market_type_ids)

    comp_result = requests.get(comps_url)
    comp_result_dict = json.loads(comp_result.content)

    ids = []
    for comp in comp_result_dict['data']['tournaments']:
        if 'id' in comp:
            ids.append(comp['id'])

    tournament_ids_template = "tournamentIds[]={tournament_id}"

    params = []
    for id in ids:
        params.append(tournament_ids_template.format(tournament_id=id))

    events_url = f"https://www.bet7.com/iapi/sportsbook/v2/sports/{sport_id}/events?timespan=24&{'&'.join(params)}&{market_type_ids}"

    result = requests.get(events_url)
    result_dict = json.loads(result.content)

    tournaments = []
    if 'data' in result_dict and 'tournaments' in result_dict['data']:
        tournaments = result_dict['data']['tournaments']

    events = []

    for t in tournaments:
        if 'events' in t:
            events.extend(t['events'])

    return events


def convert_time(iso_format):
    dt = datetime.fromisoformat(iso_format)
    return dt.timestamp() * 1000


def get_total_goals_market(event):

    markets = [market for market in event['markets'] if market['type'] == 18]

    double_result_market_1_5 = [market for market in markets if market['specifiers'][0]['value'] == '1.5']
    double_result_market_2_5 = [market for market in markets if market['specifiers'][0]['value'] == '2.5']
    double_result_market_3_5 = [market for market in markets if market['specifiers'][0]['value'] == '3.5']

    markets = []
    if len(double_result_market_1_5) == 1:
        market = {
            'name': 'total_goals_1.5',
            'selections': []
        }

        under_selection = [odd for odd in double_result_market_1_5[0]['odds'] if 'menos' in odd['name']][0]
        over_selection = [odd for odd in double_result_market_1_5[0]['odds'] if 'mais' in odd['name']][0]

        market['selections'].append({
            'name': over_selection['name'],
            'price': float(over_selection['value'])
        })

        market['selections'].append({
            'name': under_selection['name'],
            'price': float(under_selection['value'])
        })

        markets.append(market)

    if len(double_result_market_2_5) == 1:
        market = {
            'name': 'total_goals_2.5',
            'selections': []
        }

        under_selection = [odd for odd in double_result_market_2_5[0]['odds'] if 'menos' in odd['name']][0]
        over_selection = [odd for odd in double_result_market_2_5[0]['odds'] if 'mais' in odd['name']][0]

        market['selections'].append({
            'name': over_selection['name'],
            'price': float(over_selection['value'])
        })

        market['selections'].append({
            'name': under_selection['name'],
            'price': float(under_selection['value'])
        })

        markets.append(market)

    if len(double_result_market_3_5) == 1:
        market = {
            'name': 'total_goals_3.5',
            'selections': []
        }

        under_selection = [odd for odd in double_result_market_3_5[0]['odds'] if 'menos' in odd['name']][0]
        over_selection = [odd for odd in double_result_market_3_5[0]['odds'] if 'mais' in odd['name']][0]

        market['selections'].append({
            'name': over_selection['name'],
            'price': float(over_selection['value'])
        })

        market['selections'].append({
            'name': under_selection['name'],
            'price': float(under_selection['value'])
        })

        markets.append(market)

    return markets


def get_double_result_markets(event, h2h_market):
    double_result_market = [market for market in event['markets'] if market['type'] == 10]
    if len(double_result_market) <= 0:
        return None

    selection_1x = [selection for selection in double_result_market[0]['odds'] if selection['type'] == 9][0]
    selection_12 = [selection for selection in double_result_market[0]['odds'] if selection['type'] == 10][0]
    selection_x2 = [selection for selection in double_result_market[0]['odds'] if selection['type'] == 11][0]

    market = {
        'name': '1x 2',
        'selections': [
            {
                'name': selection_1x['name'],
                'price': float(selection_1x['value'])
            },
            {
                'name': h2h_market['selections'][2]['name'],
                'price': h2h_market['selections'][2]['price']
            }
        ]
    }

    market2 = {
        'name': '1 x2',
        'selections': [
            {
                'name': h2h_market['selections'][0]['name'],
                'price': h2h_market['selections'][0]['price']
            },
            {
                'name': selection_x2['name'],
                'price': float(selection_x2['value'])
            }
        ]
    }

    market3 = {
        'name': '12 x',
        'selections': [
            {
                'name': selection_12['name'],
                'price': float(selection_12['value'])
            },
            {
                'name': h2h_market['selections'][1]['name'],
                'price': h2h_market['selections'][1]['price']
            }
        ]
    }

    if len(market['selections']) != 2 or len(market2['selections']) != 2 or len(market3['selections']) != 2:
        return None

    return [market, market2, market3]
