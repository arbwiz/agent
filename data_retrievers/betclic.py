import requests
import json
import datetime

def betclic_tennis_win_match(): 
    result = requests.get("https://offer.cdn.begmedia.com/api/pub/v4/sports/2?application=1024&countrycode=pt&hasSwitchMtc=true&language=pt&limit=150&markettypeId=2013&offset=0&sitecode=ptpt&sortBy=ByLiveRankingPreliveDate")
    
    resultDict = json.loads(result.content)

    events = []
    for event in resultDict['matches']:
        event_data = {
            'bookmaker': 'betclic',
            'name': event['name'],
            'selections': [],
            'start_time': event['date'],
            'start_time_ms': round(convert_time(event['date']))
        }

        if len(event['grouped_markets']) == 0 or len(event['grouped_markets'][0]['markets']) == 0:
            continue

        for selection in event['grouped_markets'][0]['markets'][0]['selections']:
            if len(selection) == 0:
                break

            event_data['selections'].append({
                'name': selection[0]['name'],
                'price': float(selection[0]['odds'])
            })
        if len(event_data['selections']) != 2:
            continue
        events.append(event_data)
    return events

def betclic_football(): 
    result = requests.get("https://offer.cdn.begmedia.com/api/pub/v4/sports/1?application=1024&countrycode=pt&hasSwitchMtc=true&language=pt&limit=300&markettypeId=1365&offset=0&sitecode=ptpt&sortBy=ByLiveRankingPreliveDate")
    
    resultDict = json.loads(result.content)

    events = []
    for event in resultDict['matches']:
        event_data = {
            'bookmaker': 'betclic',
            'name': event['name'],
            'selections': [],
            'start_time': event['date'],
            'start_time_ms': round(convert_time(event['date']))
        }

        if len(event['grouped_markets']) == 0 or len(event['grouped_markets'][0]['markets']) == 0:
            continue

        if event['grouped_markets'][0]['markets'][0]['market_type_code'] != 'Ftb_Mr3' or len(event['grouped_markets'][0]['markets'][0]['selections']) != 3:
            continue
        
        for selection in event['grouped_markets'][0]['markets'][0]['selections']:
            if len(selection) == 0:
                break

            event_data['selections'].append({
                'name': selection[0]['name'],
                'price': float(selection[0]['odds'])
            })
        if len(event_data['selections']) != 3:
            continue
        events.append(event_data)
    return events

def convert_time(isoFormat):
    dt = datetime.datetime.fromisoformat(isoFormat)
    return(dt.timestamp()*1000)