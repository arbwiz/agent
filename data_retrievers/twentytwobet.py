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
        
        over_under_markets = get_total_over_under_goals_markets(event)

        for m in over_under_markets:
             event_data['markets'].append(m)


        events.append(event_data)
    return events

def convert_time(seconds):
    dt = datetime.datetime.fromtimestamp(seconds)
    return(dt.isoformat())

def find_market_by_id(markets, id): 
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None

def get_total_over_under_goals_markets(event):
    selections_1_5 = []
    selections_2_5 = []
    selections_3_5 = []

    for selection in event['E']:

        if 'P' in selection:
            if selection['P'] == 1.5:
                selections_1_5.append(selection)
            
            elif selection['P'] == 2.5:
                selections_2_5.append(selection)

            elif selection['P'] == 3.5:
                selections_3_5.append(selection)
        else:
            continue

    markets = []

    if(len(selections_1_5) == 2):

        market_data_1_5 = {
            'name': 'total_goals_1.5',
            'selections': []
        }

        market_data_1_5['selections'].insert(0, ({
                        'name': 'Acima de 1.5',
                        'price': float(selections_1_5[0]['C'])
                    }))
        
        market_data_1_5['selections'].insert(1, ({
                        'name': 'Abaixo de 1.5',
                        'price': float(selections_1_5[1]['C'])
                    }))
        
        markets.append(market_data_1_5)

    if(len(selections_2_5) == 2):

        market_data_2_5 = {
            'name': 'total_goals_2.5',
            'selections': []
        }

        market_data_2_5['selections'].insert(0, ({
                        'name': 'Acima de 2.5',
                        'price': float(selections_2_5[0]['C'])
                    }))
        
        market_data_2_5['selections'].insert(1, ({
                        'name': 'Abaixo de 2.5',
                        'price': float(selections_2_5[1]['C'])
                    }))
        
        markets.append(market_data_2_5)
        
    if(len(selections_3_5) == 2):

        market_data_3_5 = {
            'name': 'total_goals_3.5',
            'selections': []
        }

        market_data_3_5['selections'].insert(0, ({
                        'name': 'Acima de 3.5',
                        'price': float(selections_3_5[0]['C'])
                    }))
        
        market_data_3_5['selections'].insert(1, ({
                        'name': 'Abaixo de 3.5',
                        'price': float(selections_3_5[1]['C'])
                    }))
        
        markets.append(market_data_3_5)
    return markets