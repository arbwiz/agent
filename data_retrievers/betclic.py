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
    # should make this async
    h2h_events = request_events(1365)
    total_goals_events = request_events(411)
    double_result_events = request_events(1348)

    events = []
    for event in h2h_events:

        total_goals_event = find_event_by_id(total_goals_events, event['id'])
        double_results_event = find_event_by_id(double_result_events, event['id'])

        event_data = {
            'bookmaker': 'betclic',
            'name': event['name'],
            'markets': get_markets(event, total_goals_event, double_results_event),
            'start_time': event['date'],
            'start_time_ms': round(convert_time(event['date']))
        }

        if len(event_data['markets']) == 0:
            continue
        
        events.append(event_data)
    return events

def betclic_football_total_goals(): 
    total_goals_market_id = 411
    result = requests.get("https://offer.cdn.begmedia.com/api/pub/v4/sports/1?application=1024&countrycode=pt&hasSwitchMtc=true&language=pt&limit=300&markettypeId=" + 
                          str(total_goals_market_id) + 
                          "&offset=0&sitecode=ptpt&sortBy=ByLiveRankingPreliveDate")
    
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

        if event['grouped_markets'][0]['markets'][0]['market_type_code'] != 'Ftb_10' or len(event['grouped_markets'][0]['markets'][0]['selections'][0]) != 2:
            continue
        
        for selection in event['grouped_markets'][0]['markets'][0]['selections'][0]:
            if len(selection) == 0:
                break

            event_data['selections'].append({
                'name': selection['name'],
                'price': float(selection['odds'])
            })
        if len(event_data['selections']) != 2:
            continue
        events.append(event_data)
    return events

def get_markets(event):
    markets = []

    h2h_market = get_h2h_market(event)
    total_goals_market = get_total_goals_market(event)
    double_result_markets = get_double_result_markets(event, h2h_market)

    
    return markets

def request_events(market_type_id):
    url = ("https://offer.cdn.begmedia.com/api/pub/v4/sports/1?application=1024&countrycode=pt&hasSwitchMtc=true&language=pt&limit=300&markettypeId=" + 
           str(market_type_id) + 
           "&offset=0&sitecode=ptpt&sortBy=ByLiveRankingPreliveDate")
    
    result = requests.get(url)
    resultDict = json.loads(result.content)
    return resultDict['matches']



def get_h2h_market(event):
    market = {
        'name': 'h2h',
        'selections': []
    }

    if len(event['grouped_markets']) == 0 or len(event['grouped_markets'][0]['markets']) == 0:
        return None

    if event['grouped_markets'][0]['markets'][0]['market_type_code'] != 'Ftb_Mr3' or len(event['grouped_markets'][0]['markets'][0]['selections']) != 3:
        return None
    
    for selection in event['grouped_markets'][0]['markets'][0]['selections']:
        if len(selection) == 0:
            break

        market['selections'].append({
            'name': selection[0]['name'],
            'price': float(selection[0]['odds'])
        })

    if len(market['selections']) != 3:
        return None
    
    return market

def get_total_goals_market(event):
    market = {
        'name': 'total_goals',
        'selections': []
    }

    if len(event['grouped_markets']) == 0 or len(event['grouped_markets'][0]['markets']) == 0:
        return None

    if event['grouped_markets'][0]['markets'][0]['market_type_code'] != 'Ftb_Mr3' or len(event['grouped_markets'][0]['markets'][0]['selections']) != 3:
        return None
    
    for selection in event['grouped_markets'][0]['markets'][0]['selections']:
        if len(selection) == 0:
            break

        market['selections'].append({
            'name': selection[0]['name'],
            'price': float(selection[0]['odds'])
        })

    if len(market['selections']) != 3:
        return None
    
    return market

def get_double_result_markets(event, h2h_market):
    return[]


def convert_time(isoFormat):
    dt = datetime.datetime.fromisoformat(isoFormat)
    return(dt.timestamp()*1000)

def find_event_by_id(events, id): 
    return [event for event in events if event['id'] == id][0] 