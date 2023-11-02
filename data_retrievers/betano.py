import json
import requests
import datetime
from data_retrievers.common import scrape_website, is_valid_basket_event
from data_retrievers.common import is_valid_tennis_event
from data_retrievers.common import is_valid_football_event


async def betano_tennis_win_match_24h():
    url = 'https://www.betano.pt/sport/tenis/jogos-de-hoje/'
    soup = scrape_website(url)

    data = soup.find('body').find('script').text
    json_end = data.rfind('}')
    json_start = data.find('{')

    main_data = json.loads(data[json_start:json_end + 1])

    events = []
    for block in main_data['data']['blocks']:
        for event in block['events']:
            event_data = {
                'bookmaker': 'betano',
                'competition': event['leagueDescription'],
                'name': event['name'],
                'markets': [{
                    'name': 'h2h',
                    'selections': []
                }],
                'start_time': str(convert_time(event['startTime'])),
                'start_time_ms': event['startTime'],
                'url': 'https://www.betano.pt' + event['url']
            }
            for market in event['markets']:
                if market['name'] == 'Vencedor':
                    for selection in market['selections']:
                        event_data['markets'][0]['selections'].append({
                            'name': selection['name'],
                            'price': float(selection['price'])
                        })
            if is_valid_tennis_event(event_data):
                events.append(event_data)

    return events

async def betano_american_football():
    url = 'https://www.betano.pt/api/sport/futebol-americano/ligas/1611,10116/?req=la,s,stnf,c,mb'
    result = requests.get(url)
    main_data = json.loads(result.content)

    events = []
    for block in main_data['data']['blocks']:
        for event in block['events']:
            event_data = {
                'bookmaker': 'betano',
                'competition': event['regionName'],
                'name': event['name'],
                'markets': [{
                    'name': 'h2h',
                    'selections': []
                }],
                'start_time': str(convert_time(event['startTime'])),
                'start_time_ms': event['startTime'],
                'url': 'https://www.betano.pt' + event['url']
            }
            for market in event['markets']:
                if market['name'] == 'Vencedor':
                    for selection in market['selections']:
                        event_data['markets'][0]['selections'].append({
                            'name': selection['name'],
                            'price': float(selection['price'])
                        })
            if is_valid_basket_event(event_data):
                events.append(event_data)

    return events

async def betano_basket():
    url = 'https://www.betano.pt/api/sport/basquetebol/jogos-de-hoje/?sort=Leagues&req=la,s,stnf,c,mb'
    result = requests.get(url)
    main_data = json.loads(result.content)

    events = []
    for block in main_data['data']['blocks']:
        for event in block['events']:
            event_data = {
                'bookmaker': 'betano',
                'competition': event['regionName'],
                'name': event['name'],
                'markets': [{
                    'name': 'h2h',
                    'selections': []
                }],
                'start_time': str(convert_time(event['startTime'])),
                'start_time_ms': event['startTime'],
                'url': 'https://www.betano.pt' + event['url']
            }
            for market in event['markets']:
                if market['name'] == 'Vencedor':
                    for selection in market['selections']:
                        event_data['markets'][0]['selections'].append({
                            'name': selection['name'],
                            'price': float(selection['price'])
                        })
            if is_valid_basket_event(event_data):
                events.append(event_data)

    return events

async def betano_volley():
    url = 'https://www.betano.pt/api/sport/voleibol/jogos-de-hoje/?sort=Leagues&req=la,s,stnf,c,mb'
    result = requests.get(url)
    main_data = json.loads(result.content)

    events = []
    for block in main_data['data']['blocks']:
        for event in block['events']:
            event_data = {
                'bookmaker': 'betano',
                'competition': event['regionName'],
                'name': event['name'],
                'markets': [{
                    'name': 'h2h',
                    'selections': []
                }],
                'start_time': str(convert_time(event['startTime'])),
                'start_time_ms': event['startTime'],
                'url': 'https://www.betano.pt' + event['url']
            }
            for market in event['markets']:
                if market['name'] == 'Vencedor do jogo':
                    for selection in market['selections']:
                        event_data['markets'][0]['selections'].append({
                            'name': selection['name'],
                            'price': float(selection['price'])
                        })
            if is_valid_basket_event(event_data):
                events.append(event_data)

    return events


async def betano_football():
    url = 'https://www.betano.pt/api/sport/futebol/jogos-de-hoje/?sort=Leagues&req=la,s,stnf,c,mb'

    result = requests.get(url)

    main_data = json.loads(result.content)

    events = []
    for block in main_data['data']['blocks']:
        for event in block['events']:
            event_data = {
                'bookmaker': 'betano',
                'competition': event['leagueDescription'],
                'name': event['name'],
                'markets': [],
                'start_time': str(convert_time(event['startTime'])),
                'start_time_ms': event['startTime'],
                'url': 'https://www.betano.pt' + event['matchComboUrl']
            }
            if not event['markets']:
                break
            for market in event['markets']:
                if market['type'] == 'MRES' or market['type'] == 'MR12':
                    market_data = {
                        'name': 'h2h',
                        'selections': []
                    }
                    for selection in market['selections']:
                        market_data['selections'].append({
                            'name': selection['fullName'],
                            'price': float(selection['price'])
                        })

                    if len((market_data['selections'])) != 3:
                        continue

                    event_data['markets'].append(market_data)

                if market['type'] == 'HCTG':
                    if market['handicap'] == 1.5:
                        market_data_3_5 = create_market(market, 1.5)
                        event_data['markets'].append(market_data_3_5)
                        continue
                    if market['handicap'] == 2.5:
                        market_data_3_5 = create_market(market, 2.5)
                        event_data['markets'].append(market_data_3_5)
                        continue
                    if market['handicap'] == 3.5:
                        market_data_3_5 = create_market(market, 3.5)
                        event_data['markets'].append(market_data_3_5)
                        continue

                if market['type'] == 'DBLC':

                    h2h_market = find_market_by_id(event_data['markets'], 'h2h')

                    if h2h_market is None:
                        continue

                    market_data = {
                        'name': '1x 2',
                        'selections': [
                            {
                                'name': '1x',
                                'price': float(market['selections'][0]['price'])
                            },
                            {
                                'name': '2',
                                'price': h2h_market['selections'][2]['price']
                            }
                        ]
                    }

                    market_data2 = {
                        'name': '1 x2',
                        'selections': [
                            {
                                'name': '1',
                                'price': h2h_market['selections'][0]['price']
                            },
                            {
                                'name': 'x2',
                                'price': float(market['selections'][1]['price'])
                            }
                        ]
                    }

                    market_data3 = {
                        'name': '12 x',
                        'selections': [
                            {
                                'name': '12',
                                'price': float(market['selections'][2]['price'])
                            },
                            {
                                'name': 'x',
                                'price': h2h_market['selections'][1]['price']
                            }

                        ]
                    }
                    event_data['markets'].append(market_data)
                    event_data['markets'].append(market_data2)
                    event_data['markets'].append(market_data3)

            if is_valid_football_event(event_data):
                events.append(event_data)
    return events


def convert_time(millis):
    dt = datetime.datetime.fromtimestamp(millis / 1000)
    return (dt.isoformat())


def find_market_by_id(markets, id):
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None


def create_market(market, handicap):
    market_data = {
        'name': 'total_goals_' + str(handicap),
        'selections': []
    }

    for selection in market['selections']:
        if 'Mais' in selection['name']:
            market_data['selections'].append({
                'name': 'Over ' + str(handicap),
                'price': float(selection['price'])
            })
        elif 'Menos' in selection['name']:
            market_data['selections'].append({
                'name': 'Under ' + str(handicap),
                'price': float(selection['price'])
            })

    if len((market_data['selections'])) != 2:
        return None

    return market_data


def request_events(market_type_id):
    url = (
            "https://offer.cdn.begmedia.com/api/pub/v4/sports/1?application=1024&countrycode=pt&hasSwitchMtc=true&language=pt&limit=300&markettypeId=" +
            str(market_type_id) +
            "&offset=0&sitecode=ptpt&sortBy=ByLiveRankingPreliveDate")

    result = requests.get(url)
    resultDict = json.loads(result.content)
    return resultDict['matches']
