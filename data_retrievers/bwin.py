
import requests
import json
import datetime
import brotli

def bwin_football():
    
    url = "https://sports.bwin.pt/cds-api/bettingoffer/fixtures?x-bwin-accessid=YmQwNTFkNDAtNzM3Yi00YWIyLThkNDYtYWFmNGY2N2Y1OWIx&lang=pt&country=PT&userCountry=PT&fixtureTypes=Standard&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable&sportIds=4&regionIds=&competitionIds=&conferenceIds=&isPriceBoost=false&statisticsModes=None&skip=0&take=100&sortBy=Tags"


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Ch-Ua': 'Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'Windows',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    response = requests.get(url, headers=headers)

    res_dict = json.loads(response.content)
    
    bwin_events = res_dict['fixtures']

    events = []
    for event in bwin_events:
        if event['stage'] == 'Live':
            continue

        event_data = {
            'bookmaker': 'bwin',
            'name': event['name']['value'],
            'selections': [],
            'start_time': event['startDate'],
            'start_time_ms': round(convert_time(event['startDate']))
        }

        for option_market in event['optionMarkets']:
            if option_market['name']['value'] == 'Resultado do jogo':
                for selection in option_market['options']:
                    event_data['selections'].append({
                        'name': selection['name']['value'],
                        'price': float(selection['price']['odds'])
                    })
            break

        if len(event_data['selections']) != 3:
            continue
        events.append(event_data)
    return events


def convert_time(isoFormat):
    dt = datetime.datetime.fromisoformat(isoFormat)
    return(dt.timestamp()*1000)