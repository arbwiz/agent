import websockets
import json
import datetime


async def solverde_tennis():
    tenis_code = "067"
    return await retrieve_info_websocket(tenis_code)


async def retrieve_info_websocket(sport_id):
    ws = await websockets.connect(f"wss://sportswidget.solverde.pt/api/{sport_id}/j5uargcx/websocket", max_size=5000000)
    await ws.recv()

    init_message = "[\"CONNECT\\nprotocol-version:1.5\\naccept-version:1.0,1.1,1.2\\nheart-beat:10000,10000\\n\\n\\u0000\"]"
    init_message_2 = "[\"SUBSCRIBE\\nid:\/user\/request-response\\ndestination:\/user\/request-response\\n\\n\\u0000\"]"
    tennis_events_message = "[\"SUBSCRIBE\\nid:\/api\/eventgroups\/tennis-custom-span-48h-events\\nlocale:pt\\ndestination:\/api\/eventgroups\/tennis-custom-span-48h-events\\n\\n\\u0000\"]"
    single_event_message_template = "[\"SUBSCRIBE\\nid:\/api\/events\/{event_id}\\nlocale:pt\\ndestination:\/api\/events\/{event_id}\\n\\n\\u0000\"]"
    single_market_message_template = "[\"SUBSCRIBE\\nid:\/api\/markets\/{market_id}\\nlocale:pt\\ndestination:\/api/markets\/{market_id}\\n\\n\\u0000\"]"

    # h2h market is 97
    id_to_get_winner_market = "97"

    await ws.send(init_message)
    data1 = await ws.recv()
    await ws.send(init_message_2)
    data2 = await ws.recv()

    await ws.send(tennis_events_message)
    events_response = await ws.recv()
    events = json.loads(events_response[events_response.find("{"):events_response.rfind("}") + 1].replace("\\", ""))

    event_ids = []

    events_to_return = []

    for group in events['groups']:
        for event in group['events']:
            event_ids.append(event['id'])
            await ws.send(single_event_message_template.format(event_id=event['id']))
            event_response = await ws.recv()
            event_dict = json.loads(
                event_response[event_response.find("{"):event_response.rfind("}") + 1].replace("\\", ""))

            event_data = {
                'bookmaker': 'solverde',
                'name': event_dict['name'],
                'markets': [{
                    'name': 'h2h',
                    'selections': []
                }],
                'start_time': event_dict['startTime'],
                'start_time_ms': round(convert_time(event_dict['startTime']))
            }

            market_id = event_dict['marketTypesToIds'][id_to_get_winner_market][0]
            await ws.send(single_market_message_template.format(market_id=market_id))
            market_response = await ws.recv()

            market = json.loads(
                market_response[market_response.find("{"):market_response.rfind("}") + 1].replace("\\", ""))

            for selection in market['selections']:
                event_data['markets'][0]['selections'].append({
                    'name': selection['name'],
                    'price': float(selection['prices'][0]['decimalLabel'])
                })

            if len(event_data['markets'][0]['selections']) != 2:
                continue

            events_to_return.append(event_data)

    return events_to_return


def convert_time(isoFormat):
    dt = datetime.datetime.fromisoformat(isoFormat)
    return (dt.timestamp() * 1000)


def convert_time(isoFormat):
    dt = datetime.datetime.fromisoformat(isoFormat)
    return (dt.timestamp() * 1000)
