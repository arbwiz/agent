import requests
import json
import datetime

blacklisted_outcome1 = ['Home (Apostas especiais)', 'Equipa da Casa']
blacklisted_outcome2 = ['Convidados (especial)', 'Equipa visitante']

def twentytwobet_tennis_win_match(): 
    result = requests.get("https://22win88.com/LineFeed/Get1x2_VZip?sports=4&count=150&lng=pt&tf=3000000&tz=1&mode=4&country=148&partner=151&getEmpty=true")
    
    resultDict = json.loads(result.content)

    events = []
    for event in resultDict['Value']:

        event_data = {
            'bookmaker': '22bet',
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S']*1000
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for selection in event['E']:
            if selection['T'] == 1:
                market_data['selections'].insert(0, {
                    'name': event['O1'],
                    'price': float(selection['C'])
                })
            
            elif selection['T'] == 3:
                market_data['selections'].insert(1, {
                    'name': event['O2'],
                    'price': float(selection['C'])
                })

        if len(market_data['selections']) != 2:
            continue
        event_data['markets'] = [market_data]

        events.append(event_data)
    return events

def twentytwobet_football(): 
    #only retrieves 50 events and no pagination
    result = requests.get("https://22win88.com/LineFeed/Get1x2_VZip?sports=1&count=300&lng=pt&tf=3000000&tz=1&mode=4&country=148&partner=151&getEmpty=true")
    
    resultDict = json.loads(result.content)

    events = []
    for event in resultDict['Value']:
        event_data = {
            'bookmaker': '22bet',
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S']*1000
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }
        
        if len(event['E']) == 0:
            continue

        for selection in event['E']:
            if selection['T'] == 1:
                market_data['selections'].insert(0, ({
                    'name': event['O1'],
                    'price': float(selection['C'])
                }))
            
            elif selection['T'] == 2:
                market_data['selections'].insert(1, ({
                    'name': 'Empate',
                    'price': float(selection['C'])
                }))
            elif selection['T'] == 3:
                market_data['selections'].insert(2, ({
                    'name': event['O2'],
                    'price': float(selection['C'])
                }))

        if len(market_data['selections']) != 3  or market_data['selections'][0]['name'] in blacklisted_outcome1  or market_data['selections'][2]['name'] in blacklisted_outcome2:
            continue
        event_data['markets'] = [market_data]
        
        events.append(event_data)
    return events

def convert_time(seconds):
    dt = datetime.datetime.fromtimestamp(seconds)
    return(dt.isoformat())

def find_market_by_id(markets, id): 
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None