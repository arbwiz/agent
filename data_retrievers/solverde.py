import traceback

import websockets
import json
import datetime
import websockets
import asyncio

from data_retrievers.common import is_valid_tennis_event, is_valid_football_event, is_valid_basket_event


async def solverde_basket():
    basket_url = "wss://sportswidget.solverde.pt/api/147/apffea14/websocket"
    basket_events_message = "[\"SUBSCRIBE\\nid:\/api\/eventgroups\/basketball-custom-span-48h-events\\nlocale:pt\\ndestination:\/api\/eventgroups\/basketball-custom-span-48h-events\\n\\n\\u0000\"]"
    # tennis h2h market is 97
    id_to_get_winner_market = "97"
    return await retrieve_info_websocket_tennis("solverde", basket_url, id_to_get_winner_market, basket_events_message,
                                                'basket')


async def solverde_tennis():
    tenis_url = "wss://sportswidget.solverde.pt/api/980/qrvp3bgt/websocket"
    tennis_events_message = "[\"SUBSCRIBE\\nid:\/api\/eventgroups\/tennis-custom-span-48h-events\\nlocale:pt\\ndestination:\/api\/eventgroups\/tennis-custom-span-48h-events\\n\\n\\u0000\"]"
    # tennis h2h market is 97
    id_to_get_winner_market = "97"
    return await retrieve_info_websocket_tennis("solverde", tenis_url, id_to_get_winner_market, tennis_events_message,
                                         'tennis')


async def solverde_football():
    football_url = "wss://sportswidget.solverde.pt/api/067/j5uargcx/websocket"
    football_events_message = "[\"SUBSCRIBE\\nid:\/api\/eventgroups\/soccer-custom-span-48h-events\\nlocale:pt\\ndestination:\/api\/eventgroups\/soccer-custom-span-48h-events\\n\\n\\u0000\"]"
    # tennis h2h market is 1
    id_to_get_winner_market = '1'
    id_to_get_double_result_market = '2'
    id_to_get_total_goals_markets = '18'
    data = await retrieve_info_websocket_football("solverde", football_url,
                                         id_to_get_winner_market,
                                         football_events_message,
                                         'football',
                                         id_to_get_total_goals_markets,
                                         id_to_get_double_result_market)
    return data

async def retrieve_info_websocket_tennis(bookmaker, url, id_to_get_winner_market, events_message, sport):
    ws = await asyncio.wait_for(websockets.connect(url, max_size=5000000), 20)
    await ws.recv()

    init_message = "[\"CONNECT\\nprotocol-version:1.5\\naccept-version:1.0,1.1,1.2\\nheart-beat:10000,10000\\n\\n\\u0000\"]"
    init_message_2 = "[\"SUBSCRIBE\\nid:\/user\/request-response\\ndestination:\/user\/request-response\\n\\n\\u0000\"]"
    single_event_message_template = "[\"SUBSCRIBE\\nid:\/api\/events\/{event_id}\\nlocale:pt\\ndestination:\/api\/events\/{event_id}\\n\\n\\u0000\"]"
    single_market_message_template = "[\"SUBSCRIBE\\nid:\/api\/markets\/{market_id}\\nlocale:pt\\ndestination:\/api/markets\/{market_id}\\n\\n\\u0000\"]"

    await ws.send(init_message)
    data1 = await ws.recv()
    await ws.send(init_message_2)
    data2 = await ws.recv()

    await ws.send(events_message)
    events_response = await ws.recv()
    events = json.loads(events_response[events_response.find("{"):events_response.rfind("}") + 1].replace("\\", ""))

    event_ids = []

    event_responses = []

    for group in events['groups']:
        for event in group['events']:
            event_ids.append(event['id'])
            await ws.send(single_event_message_template.format(event_id=event['id']))
            event_response = ws.recv()
            event_responses.append(event_response)

    return await handle_event_responses_tennis(bookmaker, event_responses, id_to_get_winner_market, single_market_message_template, ws,
                                        sport)
async def retrieve_info_websocket_football(bookmaker, url, id_to_get_winner_market, events_message, sport,
                                  id_to_get_total_goals_markets=None, id_to_get_double_result_market=None):
    ws = await asyncio.wait_for(websockets.connect(url, max_size=5000000), 20)
    await ws.recv()

    init_message = "[\"CONNECT\\nprotocol-version:1.5\\naccept-version:1.0,1.1,1.2\\nheart-beat:10000,10000\\n\\n\\u0000\"]"
    init_message_2 = "[\"SUBSCRIBE\\nid:\/user\/request-response\\ndestination:\/user\/request-response\\n\\n\\u0000\"]"
    single_event_message_template = "[\"SUBSCRIBE\\nid:\/api\/events\/{event_id}\\nlocale:pt\\ndestination:\/api\/events\/{event_id}\\n\\n\\u0000\"]"
    single_market_message_template = "[\"SUBSCRIBE\\nid:\/api\/markets\/{market_id}\\nlocale:pt\\ndestination:\/api/markets\/{market_id}\\n\\n\\u0000\"]"

    await ws.send(init_message)
    data1 = await ws.recv()
    await ws.send(init_message_2)
    data2 = await ws.recv()

    await ws.send(events_message)
    events_response = await ws.recv()
    events = json.loads(events_response[events_response.find("{"):events_response.rfind("}") + 1].replace("\\", ""))

    event_ids = []

    event_responses = []

    #limit to first 15 competitions
    for group in events['groups'][:15]:
        for event in group['events']:
            event_ids.append(event['id'])
            await ws.send(single_event_message_template.format(event_id=event['id']))
            event_response = ws.recv()
            event_responses.append(event_response)

    return await handle_event_responses(bookmaker, event_responses, id_to_get_winner_market,
                                        id_to_get_total_goals_markets,
                                        id_to_get_double_result_market,
                                        single_market_message_template,
                                        ws,
                                        sport)


def convert_time(iso_format):
    dt = datetime.datetime.fromisoformat(iso_format)
    return dt.timestamp() * 1000


async def handle_event_responses(bookmaker, event_responses_t,
                                 id_to_get_winner_market,
                                 id_to_get_total_goals_markets,
                                 id_to_get_double_result_market,
                                 single_market_message_template,
                                 ws,
                                 sport):
    base_url = ""
    if sport == 'football':
        base_url = 'https://www.placard.pt/apostas/sports/soccer/events/'
    elif sport == 'basket':
        base_url = 'https://www.placard.pt/apostas/sports/basketball/events/'
    elif sport == 'tennis':
        base_url = 'https://www.placard.pt/apostas/sports/tennis/events/'

    event_responses = []
    event_with_markets = []
    for event_response_t in event_responses_t:
        event_responses.append(await event_response_t)

    for event_response in event_responses:

        event_dict = json.loads(
            event_response[event_response.find("{"):event_response.rfind("}") + 1].replace("\\", ""))

        if 'name' not in event_dict or 'startTime' not in event_dict:
            continue

        event_data = {
            'bookmaker': bookmaker,
            'competition': event_dict['canonicalTypeName'] + ' - ' + event_dict['canonicalClassName'],
            'name': event_dict['name'],
            'markets': [],
            'start_time': event_dict['startTime'],
            'start_time_ms': round(convert_time(event_dict['startTime'])),
            'url': base_url + str(event_dict['id'])
        }

        if id_to_get_winner_market not in event_dict['marketTypesToIds']:
            continue

        market_id = event_dict['marketTypesToIds'][id_to_get_winner_market][0]

        additional_markets = []

        # h2h market
        await ws.send(single_market_message_template.format(market_id=market_id))
        market_response_t = ws.recv()

        if id_to_get_double_result_market in event_dict['marketTypesToIds']:
            double_results_markets_id = event_dict['marketTypesToIds'][id_to_get_double_result_market][0]
            await ws.send(single_market_message_template.format(market_id=double_results_markets_id))
            total_goals_market_t = ws.recv()
            additional_markets.append(total_goals_market_t)

        if id_to_get_total_goals_markets in event_dict['marketTypesToIds']:
            total_goals_markets_ids = event_dict['marketTypesToIds'][id_to_get_total_goals_markets]
            for m_id in total_goals_markets_ids:
                await ws.send(single_market_message_template.format(market_id=m_id))
                total_goal_market_t = ws.recv()
                additional_markets.append(total_goal_market_t)

        m = {
            "event_data": event_data,
            "markets_tasks": [market_response_t],
            "markets_responses": []
        }

        m['markets_tasks'].extend(additional_markets)

        event_with_markets.append(m)
    return await handle_market_responses(event_with_markets, sport)


async def handle_market_responses(event_with_markets, sport):
    events_to_return = []

    for event_with_market in event_with_markets:
        for market_task in event_with_market['markets_tasks']:
            event_with_market['markets_responses'].append(await market_task)

    for event_with_market in event_with_markets:
        for market_response in event_with_market['markets_responses']:
            market = json.loads(
                market_response[market_response.find("{"):market_response.rfind("}") + 1].replace("\\", ""))

            if 'selections' not in market:
                continue

            if market['typeCategory'] == 'TEAM_HDA':

                event_with_market['event_data']['markets'].insert(0, {
                    'name': 'h2h',
                    'selections': []
                })

                for selection in market['selections']:
                    event_with_market['event_data']['markets'][0]['selections'].append({
                        'name': selection['name'],
                        'price': float(selection['prices'][0]['decimalLabel'])
                    })
            else:
                if len(event_with_market['event_data']['markets']) == 0:
                    continue
                additional_market = handle_additional_market(market, event_with_market['event_data']['markets'][0])
                if additional_market is not None:
                    event_with_market['event_data']['markets'].extend(additional_market)

        if sport == 'tennis':
            if is_valid_tennis_event(event_with_market['event_data']):
                events_to_return.append(event_with_market['event_data'])
        elif sport == 'football':
            if is_valid_football_event(event_with_market['event_data']):
                events_to_return.append(event_with_market['event_data'])

    return events_to_return


def handle_additional_market(market, h2h_market):
    if market['typeCategory'] == 'OVER_UNDER':
        if '1.5' in market['selections'][0]['name']:
            return [get_total_goals_market(market, '1.5')]

        elif '2.5' in market['selections'][0]['name']:
            return [get_total_goals_market(market, '2.5')]

        elif '3.5' in market['selections'][0]['name']:
            return [get_total_goals_market(market, '3.5')]

    elif market['typeCategory'] == 'DOUBLE_CHANCE':
        if h2h_market is None:
            return None
        market1 = {
            'name': '1x 2',
            'selections': [
                {
                    'name': '1x',
                    'price': float(market['selections'][0]['prices'][0]['decimalLabel'])
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
                    'price': float(market['selections'][2]['prices'][0]['decimalLabel'])
                }
            ]
        }

        market3 = {
            'name': '12 x',
            'selections': [
                {
                    'name': '12',
                    'price': float(market['selections'][1]['prices'][0]['decimalLabel'])
                },
                {
                    'name': 'x',
                    'price': h2h_market['selections'][1]['price']
                }
            ]
        }
        return [market1, market2, market3]


def get_total_goals_market(m, handicap):
    market = {
        'name': 'total_goals_' + handicap,
        'selections': []
    }

    market['selections'].append({
        'name': 'Over ' + str(handicap),
        'price': float(m['selections'][0]['prices'][0]['decimalLabel'])
    })

    market['selections'].append({
        'name': 'Under ' + str(handicap),
        'price': float(m['selections'][1]['prices'][0]['decimalLabel'])
    })

    return market

# tenis
async def handle_event_responses_tennis(bookmaker, event_responses_t, id_to_get_winner_market, single_market_message_template, ws, sport):
    base_url = ""
    if sport == 'football':
        base_url = 'https://www.placard.pt/apostas/sports/soccer/events/'
    elif sport == 'basket':
        base_url = 'https://www.placard.pt/apostas/sports/basketball/events/'
    elif sport == 'tennis':
        base_url = 'https://www.placard.pt/apostas/sports/tennis/events/'

    event_responses = []
    event_with_markets = []
    for event_response_t in event_responses_t:
        event_responses.append(await event_response_t)

    for event_response in event_responses:

        event_dict = json.loads(
            event_response[event_response.find("{"):event_response.rfind("}") + 1].replace("\\", ""))

        if 'name' not in event_dict or 'startTime' not in event_dict:
            continue

        event_data = {
            'bookmaker': bookmaker,
            'competition': event_dict['canonicalTypeName'] + ' - ' + event_dict['canonicalClassName'],
            'name': event_dict['name'],
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': event_dict['startTime'],
            'start_time_ms': round(convert_time(event_dict['startTime'])),
            'url': base_url + str(event_dict['id'])
        }

        if id_to_get_winner_market not in event_dict['marketTypesToIds']:
            continue

        market_id = event_dict['marketTypesToIds'][id_to_get_winner_market][0]

        await ws.send(single_market_message_template.format(market_id=market_id))
        market_response_t = ws.recv()

        event_with_markets.append({
            "event_data": event_data,
            "markets_tasks": [market_response_t],
            "markets_responses": []
        })

    return await handle_market_responses_tennis(event_with_markets, sport)


async def handle_market_responses_tennis(event_with_markets, sport):
    events_to_return = []

    for event_with_market in event_with_markets:
        for market_task in event_with_market['markets_tasks']:
            event_with_market['markets_responses'].append(await market_task)

    for event_with_market in event_with_markets:
        for market_response in event_with_market['markets_responses']:
            market = json.loads(
                market_response[market_response.find("{"):market_response.rfind("}") + 1].replace("\\", ""))

            if 'selections' not in market:
                continue

            for selection in market['selections']:
                if 'name' in selection and 'prices' in selection:
                    event_with_market['event_data']['markets'][0]['selections'].append({
                        'name': selection['name'],
                        'price': float(selection['prices'][0]['decimalLabel'])
                    })

            if sport == 'tennis':
                if is_valid_tennis_event(event_with_market['event_data']):
                    events_to_return.append(event_with_market['event_data'])
            elif sport == 'football':
                if is_valid_football_event(event_with_market['event_data']):
                    events_to_return.append(event_with_market['event_data'])
            elif sport == 'basket':
                if is_valid_basket_event(event_with_market['event_data']):
                    events_to_return.append(event_with_market['event_data'])

    return events_to_return
