import json
import requests
import datetime
from data_retrievers.common import scrape_website


def betano_tennis_win_match_24h():
    url = 'https://www.betano.pt/sport/tenis/jogos-de-hoje/'
    soup = scrape_website(url)

    data = soup.find('body').find('script').text
    json_end = data.rfind('}')
    json_start = data.find('{')

    main_data = json.loads(data[json_start:json_end+1])

    events = []
    for block in main_data['data']['blocks']:
        for event in block['events']:
            event_data = {
                'bookmaker': 'betano',
                'name': event['name'],
                'selections': [],
                'start_time': str(convert_time(event['startTime'])),
                'start_time_ms': event['startTime']
            }
            for market in event['markets']:
                if market['name'] == 'Vencedor':
                    for selection in market['selections']:
                        event_data['selections'].append({
                            'name': selection['name'],
                            'price': float(selection['price'])
                        })
            if len(event_data['selections']) != 2:
                continue
            events.append(event_data)
        return events


def betano_football():
    url = 'https://www.betano.pt/api/sport/futebol/jogos-de-hoje/?sort=Leagues&req=la,s,stnf,c,mb'

    result = requests.get(url)

    main_data = json.loads(result.content)

    events = []
    for block in main_data['data']['blocks']:
        for event in block['events']:
            event_data = {
                'bookmaker': 'betano',
                'name': event['name'],
                'markets': [],
                'start_time': str(convert_time(event['startTime'])),
                'start_time_ms': event['startTime']
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
                    market_data = {
                        'name': 'total_goals',
                        'selections': []
                    }
                    for selection in market['selections']:
                        market_data['selections'].append({
                            #adicionar handicap? 
                            'name': selection['name'],
                            'price': float(selection['price'])
                        })

                    if len((market_data['selections'])) != 2:
                        continue
                    
                    event_data['markets'].append(market_data)

                if market['type'] == 'DBLC':

                    h2h_market = find_market_by_id(event_data['markets'], 'h2h')

                    if h2h_market is None:
                        continue

                    market_data = {
                        'name': '1x 2',
                        'selections': [
                            {
                                'name': h2h_market['selections'][0]['name'] + ' ou empate',
                                'price': float(market['selections'][0]['price'])
                            },
                            {
                                'name': h2h_market['selections'][2]['name'],
                                'price': h2h_market['selections'][2]['price']
                            }
                        ]
                    }

                    market_data2 = {
                        'name': '1 x2',
                        'selections': [
                            {
                                'name': h2h_market['selections'][0]['name'],
                                'price': h2h_market['selections'][0]['price']
                            },
                            {
                                'name': h2h_market['selections'][2]['name'] + ' ou empate',
                                'price': float(market['selections'][1]['price'])
                            }
                        ]
                    }

                    market_data3 = {
                        'name': '12 x',
                        'selections': [
                            {
                                'name': h2h_market['selections'][0]['name'] + " ou " + h2h_market['selections'][2]['name'],
                                'price': float(market['selections'][2]['price'])
                            },
                            {
                                'name': h2h_market['selections'][1]['name'],
                                'price': h2h_market['selections'][1]['price']
                            }
                        
                        ]
                    }
                    event_data['markets'].append(market_data)
                    event_data['markets'].append(market_data2)
                    event_data['markets'].append(market_data3)

            if len(event_data['markets']) < 1:
                continue
            events.append(event_data)
    return events


def convert_time(millis):
    dt = datetime.datetime.fromtimestamp(millis/1000)
    return (dt.isoformat())

def find_market_by_id(markets, id): 
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None