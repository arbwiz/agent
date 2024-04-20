import requests
import json
import datetime

from utils import sanitize_text


def convert_time_plus2_ms(iso_plus2):
    dt = datetime.datetime.fromisoformat(iso_plus2)
    return (dt.timestamp() * 1000)


def convert_time_from_plus2_to_z(iso_plus2):
    millis = convert_time_plus2_ms(iso_plus2)
    dt = datetime.datetime.fromtimestamp(millis / 1000)
    return (dt.isoformat())


async def betway_tennis():
    url = 'https://ws.betway.pt/component/datatree'

    body = {
        "context": {
            "url_key": "/desporte/21-tenis",
            "clientIp": "5.249.83.253",
            "version": "1.0.1",
            "device": "web_vuejs_desktop",
            "lang": "pt",
            "timezone": "Europe/Lisbon",
            "url_params": {}
        }
    }

    result = requests.post(url, json=body)
    main_data = json.loads(result.content)

    events = []
    for event in main_data['tree']['components'][3]['components'][7]['data']['events']:

        event_name = event['label'].replace('/', '*').replace('-', '/').replace('*', '-')

        event_data = {
            'bookmaker': 'betway',
            'competition': event['competition']['label'],
            'name': event_name,
            'participant_a': sanitize_text(event_name.split('-')[0]),
            'participant_b': sanitize_text(event_name.split('-')[1]),
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time_from_plus2_to_z(event['start'])),
            'start_time_ms': round(convert_time_plus2_ms(event['start'])),
            'url': 'https://apostas.betway.pt' + event['url']
        }

        if len(event['bets'][0]['choices']) != 2:
            continue

        event_data['markets'][0]['selections'].append({
            'name': event['bets'][0]['choices'][0]['actor']['label'],
            'price': event['bets'][0]['choices'][0]['odd']
        })

        event_data['markets'][0]['selections'].append({
            'name': event['bets'][0]['choices'][1]['actor']['label'],
            'price': event['bets'][0]['choices'][1]['odd']
        })

        events.append(event_data)

    return events

async def betway_basket():
    url = 'https://ws.betway.pt/component/datatree'

    body = {
        "context": {
            "url_key": "/desporte/4-basquetebol",
            "clientIp": "5.249.83.253",
            "version": "1.0.1",
            "device": "web_vuejs_desktop",
            "lang": "pt",
            "timezone": "Europe/Lisbon",
            "url_params": {}
        }
    }

    result = requests.post(url, json=body)
    main_data = json.loads(result.content)

    events = []
    for event in main_data['tree']['components'][3]['components'][6]['data']['events']:

        event_name = event['label'].replace('/', '*').replace('-', '/').replace('*', '-')

        event_data = {
            'bookmaker': 'betway',
            'competition': event['competition']['label'],
            'name': event_name,
            'participant_a': sanitize_text(event_name.split('-')[0]),
            'participant_b': sanitize_text(event_name.split('-')[1]),
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time_from_plus2_to_z(event['start'])),
            'start_time_ms': round(convert_time_plus2_ms(event['start'])),
            'url': 'https://apostas.betway.pt' + event['url']
        }

        if len(event['bets'][0]['choices']) != 2:
            continue

        event_data['markets'][0]['selections'].append({
            'name': event['bets'][0]['choices'][0]['actor']['label'],
            'price': event['bets'][0]['choices'][0]['odd']
        })

        event_data['markets'][0]['selections'].append({
            'name': event['bets'][0]['choices'][1]['actor']['label'],
            'price': event['bets'][0]['choices'][1]['odd']
        })

        events.append(event_data)

    return events
