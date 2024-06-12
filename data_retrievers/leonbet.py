import requests
import json
import datetime

from utils import sanitize_text


def convert_time(millis):
    dt = datetime.datetime.fromtimestamp(millis / 1000)
    return dt.isoformat()

async def leonbet_tennis():
    url = ('https://leon76.bet/api-2/betline/events/all?ctag=pt-PT&hideClosed=true&flags=reg,urlv2,mm2,rrc,'
           'nodup&sport_id=1970324836974594')

    result = requests.get(url)
    main_data = json.loads(result.content)
    competitions_map = {}

    region_map = {
        '1970324836974693': 'wta',
        '1970324836975108': 'atp-challenger',
        '1970324836975185': 'itf-men',
        '1970324836975186': 'itf-women',
        '1970324836974594': 'atp',
        '1970324836975456': 'utr-women',
        '1970324836975589': 'olympics'
    }

    events = []
    for event in main_data['events']:

        if 'inplay' in event['betline'] or len(event['competitors']) != 2:
            continue

        participant_a = event['competitors'][0]['name']
        participant_b = event['competitors'][1]['name']

        if 'sport' in event['league']:
            region = region_map.get(str(event['league']['region']['id']))

            if region is None:
                continue

            competition = {
                'name': event['league']['nameDefault'],
                'url': region + '/' + event['league']['url'],
                'sport_id': event['league']['sport']['id']
            }
            competitions_map[event['league']['id']] = competition
        else:
            competition = competitions_map.get(event['league']['id'])

        if competition is None:
            continue
        event_data = {
            'bookmaker': 'leonbet',
            'competition': competition['name'],
            'name': event['name'],
            'participant_a': sanitize_text(participant_a),
            'participant_b': sanitize_text(participant_b),
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time(event['kickoff'])),
            'start_time_ms': event['kickoff'],
            'url': 'https://leon76.bet/bets/tennis/' + competition['url'] + '/' + str(event['id']) + event['url']
        }

        if 'market' not in event:
            continue

        for market in event['markets']:
            if 'Vencedor' != market['name'] or len(market['runners']) != 2:
                continue

            event_data['markets'][0]['selections'].append({
                'name': participant_a,
                'price': market['runners'][0]['price']
            })

            event_data['markets'][0]['selections'].append({
                'name': participant_b,
                'price': market['runners'][1]['price']
            })

            events.append(event_data)

    return events
