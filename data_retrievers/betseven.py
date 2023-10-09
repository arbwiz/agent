import json
from datetime import datetime

import requests

from data_retrievers.common import is_valid_tennis_event


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


async def get_events(sport_arg):
    sport_id = 1
    sport_name = 'Football'

    if sport_arg == 'football':
        sport_id = 1
        sport_name = 'Football'
    elif sport_arg == 'tennis':
        sport_id = 5
        sport_name = 'Tennis'
        market_type_ids = "&marketTypeIds[]=186"
    elif sport_arg == 'basket':
        sport_id = 3
        sport_name = 'Basketball'

    comps_url = (
        f"https://www.bet7.com/iapi/sportsbook/v2/sports/{sport_id}/tournaments?timespan=24{market_type_ids}").format(
        sport_id=sport_id, market_type_ids=market_type_ids)

    result = requests.get(comps_url)
    result_dict = json.loads(result.content)

    ids = []
    for comp in result_dict['data']['tournaments']:
        if 'id' in comp:
            ids.append(comp['id'])


    tournament_ids_template = "tournamentIds[]={tournament_id}"

    params = []
    for id in ids:
        params.append(tournament_ids_template.format(tournament_id=id))

    events_url = f"https://www.bet7.com/iapi/sportsbook/v2/sports/5/events?timespan=24&{'&'.join(params)}&{market_type_ids}"

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
