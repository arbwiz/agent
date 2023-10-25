import requests
import json
import datetime
import brotli

from data_retrievers.common import is_valid_tennis_event, is_valid_football_event, is_valid_basket_event

SPORT_ID_TENNIS = '5'
SPORT_ID_BASKET = '7'
SPORT_ID_FOOTBALL = '4'
BWIN_URL = "https://sports.bwin.pt/cds-api/bettingoffer/fixtures?x-bwin-accessid" \
           "=YmQwNTFkNDAtNzM3Yi00YWIyLThkNDYtYWFmNGY2N2Y1OWIx&lang=pt&country=PT&userCountry=PT&fixtureTypes=Standard" \
           "&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable&sportIds=SPORT_ID" \
           "&regionIds=&competitionIds=&conferenceIds=&isPriceBoost=false&statisticsModes=None&skip=0&take=100&sortBy" \
           "=Tags "


async def bwin_tennis():
    url = BWIN_URL.replace('SPORT_ID', SPORT_ID_TENNIS)

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
            'competition': event['competition']['name']['value'],
            'name': event['name']['value'],
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': event['startDate'],
            'start_time_ms': round(convert_time(event['startDate'])),
            'url': 'https://sports.bwin.pt/pt/sports/eventos/' + str(event['id'])
        }

        for game in event['games']:
            if game['name']['value'] == 'Vencedor do jogo':
                for selection in game['results']:
                    event_data['markets'][0]['selections'].append({
                        'name': selection['name']['value'],
                        'price': float(selection['odds'])
                    })
            break

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events

async def bwin_basket():
    url = BWIN_URL.replace('SPORT_ID', SPORT_ID_BASKET)

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
            'competition': event['competition']['name']['value'],
            'name': event['name']['value'],
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': event['startDate'],
            'start_time_ms': round(convert_time(event['startDate'])),
            'url': 'https://sports.bwin.pt/pt/sports/eventos/' + str(event['id'])
        }

        for game in event['games']:
            if game['name']['value'] == 'Vencedor do jogo':
                for selection in game['results']:
                    event_data['markets'][0]['selections'].append({
                        'name': selection['name']['value'],
                        'price': float(selection['odds'])
                    })
            break

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events

async def bwin_football():
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
            'competition': event['competition']['name']['value'],
            'name': event['name']['value'],
            'markets': [],
            'start_time': event['startDate'],
            'start_time_ms': round(convert_time(event['startDate'])),
            'url': 'https://sports.bwin.pt/pt/sports/eventos/' + str(event['id'])
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for option_market in event['optionMarkets']:
            if option_market['name']['value'] == 'Resultado do jogo':
                for selection in option_market['options']:
                    market_data['selections'].append({
                        'name': selection['name']['value'],
                        'price': float(selection['price']['odds'])
                    })
            break

        if len(market_data['selections']) != 3:
            continue
        event_data['markets'] = [market_data]


        dr_markets = get_double_result_markets(event, market_data)
        ou_markets = get_total_goals_market(event)

        if dr_markets is not None:
            event_data['markets'].extend(dr_markets)
        if ou_markets is not None:
            event_data['markets'].extend(ou_markets)

        if is_valid_football_event(event_data):
            events.append(event_data)
    return events


def get_total_goals_market(event):
    double_result_markets = [market for market in event['optionMarkets'] if market['name']['value'] == 'Total golos']

    double_result_market_1_5 = [market for market in double_result_markets if
                                '1,5' in market['options'][0]['name']['value']]
    double_result_market_2_5 = [market for market in double_result_markets if
                                '2,5' in market['options'][0]['name']['value']]
    double_result_market_3_5 = [market for market in double_result_markets if
                                '3,5' in market['options'][0]['name']['value']]

    markets = []
    if len(double_result_market_1_5) == 1:
        market = {
            'name': 'total_goals_1.5',
            'selections': []
        }

        market['selections'].append({
            'name': 'Over 1.5',
            'price': float(double_result_market_1_5[0]['options'][0]['price']['odds'])
        })

        market['selections'].append({
            'name': 'Under 1.5',
            'price': float(double_result_market_1_5[0]['options'][1]['price']['odds'])
        })

        markets.append(market)

    if len(double_result_market_2_5) == 1:
        market = {
            'name': 'total_goals_2.5',
            'selections': []
        }

        market['selections'].append({
            'name': 'Over 2.5',
            'price': float(double_result_market_2_5[0]['options'][0]['price']['odds'])
        })

        market['selections'].append({
            'name': 'Under 2.5',
            'price': float(double_result_market_2_5[0]['options'][1]['price']['odds'])
        })

        markets.append(market)

    if len(double_result_market_3_5) == 1:
        market = {
            'name': 'total_goals_3.5',
            'selections': []
        }

        market['selections'].append({
            'name': 'Over 3.5',
            'price': float(double_result_market_3_5[0]['options'][0]['price']['odds'])
        })

        market['selections'].append({
            'name': 'Under 3.5',
            'price': float(double_result_market_3_5[0]['options'][1]['price']['odds'])
        })

        markets.append(market)

    return markets


def get_double_result_markets(event, h2h_market):

    double_result_market_r = [market for market in event['optionMarkets'] if market['name']['value'] == 'Double Chance']
    if len(double_result_market_r) > 0:
        double_result_market = double_result_market_r[0]
    else:
        return None

    market = {
        'name': '1x 2',
        'selections': [
            {
                'name': '1x',
                'price': float(double_result_market['options'][0]['price']['odds'])
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
                'name': "1",
                'price': h2h_market['selections'][0]['price']
            },
            {
                'name': 'x2',
                'price': float(double_result_market['options'][1]['price']['odds'])
            }
        ]
    }

    market3 = {
        'name': '12 x',
        'selections': [
            {
                'name': '12',
                'price': float(double_result_market['options'][2]['price']['odds'])
            },
            {
                'name': 'x',
                'price': h2h_market['selections'][1]['price']
            }
        ]
    }

    if len(market['selections']) != 2 or len(market2['selections']) != 2 or len(market3['selections']) != 2:
        return None

    return [market, market2, market3]


def convert_time(iso_format):
    dt = datetime.datetime.fromisoformat(iso_format)
    return dt.timestamp() * 1000


def find_market_by_id(markets, id):
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None
