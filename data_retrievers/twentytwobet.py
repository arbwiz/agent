import requests
import json

def twentytwobet_tennis_win_match(): 
    result = requests.get("https://22win88.com/LineFeed/Get1x2_VZip?sports=4&count=150&lng=pt&tf=3000000&tz=1&mode=4&country=148&partner=151&getEmpty=true")
    
    resultDict = json.loads(result.content)

    events = []
    for event in resultDict['Value']:
        event_data = {
            'bookmaker': '22bet',
            'name': event['O1'] + ' - ' + event['O2'],
            'selections': []
        }
        for selection in event['E']:
            if selection['T'] == 1:
                event_data['selections'].append({
                    'name': event['O1'],
                    'price': float(selection['C'])
                })
            
            elif selection['T'] == 3:
                event_data['selections'].append({
                    'name': event['O2'],
                    'price': float(selection['C'])
                })
        
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
            'selections': []
        }
        for selection in event['E']:
            if selection['T'] == 1:
                event_data['selections'].append({
                    'name': event['O1'],
                    'price': float(selection['C'])
                })
            
            elif selection['T'] == 2:
                event_data['selections'].append({
                    'name': 'Empate',
                    'price': float(selection['C'])
                })
            elif selection['T'] == 3:
                event_data['selections'].append({
                    'name': event['O2'],
                    'price': float(selection['C'])
                })
        
        events.append(event_data)
    return events