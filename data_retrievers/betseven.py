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
            'competition': event['competition'],
            'name': event['participants']['home']['name'] + ' - ' + event['participants']['away']['name'],
            'markets': [],
            'start_time': event['startTime'],
            'start_time_ms': convert_time(event['startTime']),
            'url': 'https://www.bet7.com/sportsbook/5/events/' + str(event['id'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor':
                for odd in market['odds']:
                    if odd['type'] == 4:
                        market_data['selections'].insert(0, {
                            'name': odd['name'],
                            'price': float(odd['value'])
                        })
                    elif odd['type'] == 5:
                        market_data['selections'].insert(1, {
                            'name': odd['name'],
                            'price': float(odd['value'])
                        })
                break

        event_data['markets'] = [market_data]

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events


async def get_american_football_events():
    nfl = "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/31"
    cfl = "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/790"

    token_resp = requests.get(nfl)
    token = token_resp.cookies.get_dict()['XSRF-TOKEN'][:-4] + '=0'

    req_body = {
        "marketTypeIds": [223, 225, 219]
    }

    headers = {
        'Content-Type': 'application/json',
        'X-Xsrf-Token': token,
        'Cookie': 'site_session=' + token_resp.cookies.get_dict()['site_session']
    }

    nfl_resp = requests.post(cfl, json=req_body, headers=headers)
    cfl_resp = requests.post(nfl, json=req_body, headers=headers)

    cfl_result = json.loads(cfl_resp.content)
    nfl_result = json.loads(nfl_resp.content)

    events = []

    for nfl_e in nfl_result['data']['events']:
        nfl_e['competition'] = nfl_result['data']['categoryName'] + ' - ' + nfl_result['data']['tournamentName']
        events.append(nfl_e)

    for cfl_e in cfl_result['data']['events']:
        cfl_e['competition'] = cfl_result['data']['categoryName'] + ' - ' + cfl_result['data']['tournamentName']
        events.append(cfl_e)

    return events


async def betseven_american_football():
    result_events = await get_american_football_events()

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': 'betseven',
            'competition': event['competition'],
            'name': event['participants']['home']['name'] + ' - ' + event['participants']['away']['name'],
            'markets': [],
            'start_time': event['startTime'],
            'start_time_ms': convert_time(event['startTime']),
            'url': 'https://www.bet7.com/sportsbook/2/events/' + str(event['id'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor (Incluindo Prolongamento)':

                for odd in market['odds']:
                    if odd['type'] == 4:
                        market_data['selections'].insert(0, {
                            'name': odd['name'],
                            'price': float(odd['value'])
                        })
                    elif odd['type'] == 5:
                        market_data['selections'].insert(1, {
                            'name': odd['name'],
                            'price': float(odd['value'])
                        })

        event_data['markets'] = [market_data]

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events

async def betseven_basket():
    result_events = await get_events('basket')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': 'betseven',
            'competition': event['competition'],
            'name': event['participants']['home']['name'] + ' - ' + event['participants']['away']['name'],
            'markets': [],
            'start_time': event['startTime'],
            'start_time_ms': convert_time(event['startTime']),
            'url': 'https://www.bet7.com/sportsbook/2/events/' + str(event['id'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor (incluindo prorrogação)':

                for odd in market['odds']:
                    if odd['type'] == 4:
                        market_data['selections'].insert(0, {
                            'name': odd['name'],
                            'price': float(odd['value'])
                        })
                    elif odd['type'] == 5:
                        market_data['selections'].insert(1, {
                            'name': odd['name'],
                            'price': float(odd['value'])
                        })
                break

        event_data['markets'] = [market_data]

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events


async def betseven_football():
    result_events = await get_events('football')

    events = []
    for event in result_events:

        if 'Liga Realidade Simulada' in event['competition']:
            continue

        event_data = {
            'bookmaker': 'betseven',
            'competition': event['competition'],
            'name': event['participants']['home']['name'] + ' - ' + event['participants']['away']['name'],
            'markets': [],
            'start_time': event['startTime'],
            'start_time_ms': convert_time(event['startTime']),
            'url': 'https://www.bet7.com/sportsbook/1/events/' + str(event['id'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for market in event['markets']:
            if market['name'] == 'Vencedor':
                for odd in market['odds']:
                    if odd['type'] == 1:
                        market_data['selections'].insert(0, {
                            'name': odd['name'],
                            'price': float(odd['value'])
                        })
                    elif odd['type'] == 2:
                        market_data['selections'].insert(1, {
                            'name': odd['name'],
                            'price': float(odd['value'])
                        })
                    elif odd['type'] == 3:
                        market_data['selections'].insert(2, {
                            'name': odd['name'],
                            'price': float(odd['value'])
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
        f"https://www.bet7.com/iapi/sportsbook/v2/sports/{sport_id}").format(sport_id=sport_id)

    comp_result = requests.get(comps_url)
    comp_result_dict = json.loads(comp_result.content)

    ids = []
    for cat in comp_result_dict['data']['categories']:
        if 'tournaments' in cat:
            for comp in cat['tournaments']:
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
            enriched_events = []
            for e in t['events']:
                e['competition'] = t['categoryName'] + ' - ' + t['name']
                enriched_events.append(e)

            events.extend(enriched_events)

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
            'name': 'Over 1.5',
            'price': float(over_selection['value'])
        })

        market['selections'].append({
            'name': 'Under 1.5',
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
            'name': 'Over 2.5',
            'price': float(over_selection['value'])
        })

        market['selections'].append({
            'name': 'Under 2.5',
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
            'name': 'Over 3.5',
            'price': float(over_selection['value'])
        })

        market['selections'].append({
            'name': 'Under 3.5',
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
                'name': '1x',
                'price': float(selection_1x['value'])
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
                'price': float(selection_x2['value'])
            }
        ]
    }

    market3 = {
        'name': '12 x',
        'selections': [
            {
                'name': '12',
                'price': float(selection_12['value'])
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
