import websockets
import json
import uuid
import base64
import datetime


async def solverde_tennis():
    tenis_code = "067"

    data = await retrieve_info_websocket(tenis_code)

    content = json.loads(json.loads(data['Message'])['Requests'][0]['Content'])

    parsed_events = [event for league_item in content['LeagueDataSource']['LeagueItems'] for event in
                     league_item['EventItems']]

    events = []

    for event in parsed_events:
        event_data = {
            'bookmaker': 'esconline',
            'name': event['EventName'].replace(':', '-'),
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': event['StartDate'],
            'start_time_ms': round(convert_time(event['StartDate']))
        }
        for market in event['MarketItems']:
            if market['MarketName'] == 'Vencedor':
                for outcome in market['OutcomeItems']:
                    event_data['markets'][0]['selections'].append({
                        'name': outcome['Name'],
                        'price': outcome['Odd']
                    })
                break
        if len(event_data['markets'][0]['selections']) != 2:
            continue
        events.append(event_data)
    return events


async def retrieve_info_websocket(sport_id):
    ws = await websockets.connect(f"wss://sportswidget.solverde.pt/api/{sport_id}/j5uargcx/websocket", max_size=5000000)
    await ws.recv()

    init_message = "[\"CONNECT\\nprotocol-version:1.5\\naccept-version:1.0,1.1,1.2\\nheart-beat:10000,10000\\n\\n\\u0000\"]"
    init_message_2 = "[\"SUBSCRIBE\\nid:\/user\/request-response\\ndestination:\/user\/request-response\\n\\n\\u0000\"]"
    tennis_events_message = "[\"SUBSCRIBE\\nid:\/api\/eventgroups\/tennis-custom-span-48h-events\\nlocale:pt\\ndestination:\/api\/eventgroups\/tennis-custom-span-48h-events\\n\\n\\u0000\"]"
    single_event_message_template = "[\"SUBSCRIBE\nid:/api/events/{event_id}\nlocale:pt\ndestination:/api/events/{event_id}\n\n\u0000\"]"
    single_market_message_template = "[\"SUBSCRIBE\nid:/api/markets/{market_id}\nlocale:pt\ndestination:/api/markets/{market_id}\n\n\u0000\"]"

    print(init_message)
    id_to_get_winner_market = "97"

    await ws.send(init_message)
    data1 = await ws.recv()
    await ws.send(init_message_2)
    data2 = await ws.recv()
    await ws.send(tennis_events_message)
    events_response = await ws.recv()
    events = json.loads(events_response)

    return events


def convert_time(isoFormat):
    dt = datetime.datetime.fromisoformat(isoFormat)
    return (dt.timestamp() * 1000)
