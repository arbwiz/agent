import requests
import json
import datetime
import asyncio

from data_retrievers.common import is_valid_tennis_event, is_valid_football_event, is_valid_basket_event

blacklisted_outcome1 = ['Home (Apostas especiais)', 'Equipa da Casa']
blacklisted_outcome2 = ['Convidados (especial)', 'Equipa visitante']
max_comps = 10
blacklisted_comp_ids = [2150631, 2590430, 2390706, 2322382, 2498900]
whitelisted_comp_ids = {
    'football': [7067, 8777, 11113, 12821, 12829, 13521, 13709, 16819, 17555, 26031, 27687, 27707, 27731, 28787,
                 30467, 88637, 96463, 105759, 109313, 110163, 118663, 118737, 127733, 166251, 211661, 214147,
                 225733, 281719, 828065, 1015483, 1268397, 1471313, 2018750, 2151274, 2284664, 2421233],
    'tennis': []
}


async def twentytwobet_tennis_win_match():
    comps_ids = get_competition_ids('tennis')

    result_events = await get_events_from_competitions(comps_ids, 'tennis')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': '22bet',
            'competition': event['LE'],
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S'] * 1000,
            'url': 'https://22win88.com/line/tennis/' + format_url(event)
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

        event_data['markets'] = [market_data]

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events

async def twentytwobet_american_football():
    comps_ids = get_competition_ids('american_football')

    result_events = await get_events_from_competitions(comps_ids, 'american_football')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': '22bet',
            'competition': event['LE'],
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S'] * 1000,
            'url': 'https://22win88.com/line/basketball/' + format_url(event)
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
            else:
                continue

        event_data['markets'] = [market_data]

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events

async def twentytwobet_basket():
    comps_ids = get_competition_ids('basket')

    result_events = await get_events_from_competitions(comps_ids, 'basket')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': '22bet',
            'competition': event['LE'],
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S'] * 1000,
            'url': 'https://22win88.com/line/basketball/' + format_url(event)
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for selection in event['E']:
            if selection['T'] == 401:
                market_data['selections'].insert(0, {
                    'name': event['O1'],
                    'price': float(selection['C'])
                })

            elif selection['T'] == 402:
                market_data['selections'].insert(1, {
                    'name': event['O2'],
                    'price': float(selection['C'])
                })
            else:
                continue

        event_data['markets'] = [market_data]

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events

async def twentytwobet_volley():
    comps_ids = get_competition_ids('volleyball')

    result_events = await get_events_from_competitions(comps_ids, 'volleyball')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': '22bet',
            'competition': event['LE'],
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S'] * 1000,
            'url': 'https://22win88.com/line/volleyball/' + format_url(event)
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
            else:
                continue

        event_data['markets'] = [market_data]

        if is_valid_basket_event(event_data):
            events.append(event_data)
    return events

async def twentytwobet_football():
    # only retrieves 50 events and no pagination
    # result = requests.get(
    #    "https://22win88.com/LineFeed/Get1x2_VZip?sports=1&count=300&lng=pt&tf=3000000&tz=1&mode=4&country=148"
    #    "&partner=151&getEmpty=true")

    # resultDict = json.loads(result.content)

    comps_ids = get_competition_ids('football')

    result_events = await get_events_from_competitions(comps_ids, 'football')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': '22bet',
            'competition': event['LE'],
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S'] * 1000,
            'url': 'https://22win88.com/line/football/' + format_url(event)
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

        if len(market_data['selections']) != 3 or market_data['selections'][0]['name'] in blacklisted_outcome1 or \
                market_data['selections'][2]['name'] in blacklisted_outcome2:
            continue
        event_data['markets'] = [market_data]

        over_under_markets = get_total_over_under_goals_markets(event)

        double_results_markets = get_double_results_markets(event, market_data)

        for ou_market in over_under_markets:
            event_data['markets'].append(ou_market)

        for dr_market in double_results_markets:
            event_data['markets'].append(dr_market)

        if is_valid_football_event(event_data):
            events.append(event_data)
    return events


def convert_time(seconds):
    dt = datetime.datetime.fromtimestamp(seconds)
    return dt.isoformat()


def find_market_by_id(markets, id):
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None


def get_total_over_under_goals_markets(event):
    selections_1_5 = []
    selections_2_5 = []
    selections_3_5 = []

    for selection in event['E']:

        if 'P' in selection and selection['G'] == 17:
            if selection['P'] == 1.5:
                selections_1_5.append(selection)

            elif selection['P'] == 2.5:
                selections_2_5.append(selection)

            elif selection['P'] == 3.5:
                selections_3_5.append(selection)
        else:
            continue

    markets = []

    if len(selections_1_5) == 2:
        market_data_1_5 = {
            'name': 'total_goals_1.5',
            'selections': []
        }

        market_data_1_5['selections'].insert(0, ({
            'name': 'Over  1.5',
            'price': float(selections_1_5[0]['C'])
        }))

        market_data_1_5['selections'].insert(1, ({
            'name': 'Under 1.5',
            'price': float(selections_1_5[1]['C'])
        }))

        markets.append(market_data_1_5)

    if len(selections_2_5) == 2:
        market_data_2_5 = {
            'name': 'total_goals_2.5',
            'selections': []
        }

        market_data_2_5['selections'].insert(0, ({
            'name': 'Over 2.5',
            'price': float(selections_2_5[0]['C'])
        }))

        market_data_2_5['selections'].insert(1, ({
            'name': 'Under 2.5',
            'price': float(selections_2_5[1]['C'])
        }))

        markets.append(market_data_2_5)

    if len(selections_3_5) == 2:
        market_data_3_5 = {
            'name': 'total_goals_3.5',
            'selections': []
        }

        market_data_3_5['selections'].insert(0, ({
            'name': 'Over 3.5',
            'price': float(selections_3_5[0]['C'])
        }))

        market_data_3_5['selections'].insert(1, ({
            'name': 'Under 3.5',
            'price': float(selections_3_5[1]['C'])
        }))

        markets.append(market_data_3_5)
    return markets


def get_double_results_markets(event, h2h_market):
    market_data_1x_2 = None
    market_data_1_2x = None
    market_data_12_x = None

    for selection in event['E']:
        if selection['T'] == 4:
            market_data_1x_2 = {
                'name': '1x 2',
                'selections': []
            }

            market_data_1x_2['selections'].insert(0, ({
                'name': '1x',
                'price': float(selection['C'])
            }))

            market_data_1x_2['selections'].insert(1, ({
                'name': '2',
                'price': float(h2h_market['selections'][2]['price'])
            }))

        elif selection['T'] == 5:
            market_data_12_x = {
                'name': '12 x',
                'selections': []
            }

            market_data_12_x['selections'].insert(0, ({
                'name': '12',
                'price': float(selection['C'])
            }))

            market_data_12_x['selections'].insert(1, ({
                'name': 'x',
                'price': float(h2h_market['selections'][1]['price'])
            }))

        elif selection['T'] == 6:

            market_data_1_2x = {
                'name': '1 x2',
                'selections': []
            }

            market_data_1_2x['selections'].insert(0, ({
                'name': '1',
                'price': float(h2h_market['selections'][0]['price'])
            }))

            market_data_1_2x['selections'].insert(1, ({
                'name': 'x2',
                'price': float(selection['C'])
            }))

    markets = []
    if market_data_1x_2 is not None:
        markets.append(market_data_1x_2)
    if market_data_1_2x is not None:
        markets.append(market_data_1_2x)
    if market_data_12_x is not None:
        markets.append(market_data_12_x)

    return markets


def get_competition_ids(sport_arg):
    sport_id = 1
    sport_name = 'Football'

    if sport_arg == 'football':
        sport_id = 1
        sport_name = 'Football'
    elif sport_arg == 'tennis':
        sport_id = 4
        sport_name = 'Tennis'
    elif sport_arg == 'basket':
        sport_id = 3
        sport_name = 'Basketball'
    elif sport_arg == 'volleyball':
        sport_id = 6
        sport_name = 'Volleyball'
    elif sport_arg == 'american_football':
        sport_id = 13
        sport_name = 'American Football'

    comps_url = (
        f"https://22win88.com/LineFeed/GetSportsShortZip?sports={sport_id}&lng=pt&tf=2880&country=148&partner=151"
        "&virtualSports=true&group=151&gr=151").format(sport_id=sport_id)

    result = requests.get(comps_url)
    result_dict = json.loads(result.content)

    comps = []
    for sport in result_dict['Value']:
        if sport['E'] == sport_name:
            comps = sport['L']
            break

    grouped_ids = []

    number_of_games = 0
    ids = []

    if sport_arg == 'tennis':
        comps = comps[:max_comps]

    for comp in comps:
        # if number of games in comp is higher than 15, consider relevant to request

        if sport_arg == 'football' and comp['LI'] not in whitelisted_comp_ids[sport_arg]:
            continue

        number_of_games += comp['GC']

        if number_of_games >= 50:
            ids.append(comp['LI'])
            ids.sort()
            grouped_ids.append(ids)
            ids = []
            number_of_games = 0
        else:
            ids.append(comp['LI'])

    if len(grouped_ids) == 0:
        ids.sort()
        grouped_ids.append(ids)
    return grouped_ids


async def get_events_from_competitions(competition_ids, sport):
    tf = 2880
    if sport == 'football':
        mode_id = 4
        sport_id = 1
    elif sport == 'tennis':
        sport_id = 4
        mode_id = 4
    elif sport == 'basket':
        sport_id = 3
        mode_id = 1
    elif sport == 'volleyball':
        sport_id = 6
        mode_id = 1
    elif sport == 'american_football':
        sport_id = 13
        mode_id = 1
        tf = 3000000

    url_template = ("https://22win88.com/LineFeed/Get1x2_VZip?sports={sport_id}&champs={"
                    "competition_id}&count=50&lng=pt&tf={tf}&tz=1&mode={mode_id}&country=148&partner=151&getEmpty=true")
    events = []
    results_t = []

    for ids in competition_ids:
        url = url_template.format(url_template, sport_id=sport_id, competition_id=','.join(map(str, ids)),
                                  tf=tf, mode_id=mode_id)
        result_t = asyncio.create_task(req(url))
        results_t.append(result_t)

    results = []
    for result_t in results_t:
        results.append(await result_t)

    for result in results:
        result_dict = json.loads(result.content)
        events.extend(result_dict['Value'])

    return events


async def req(url):
    return requests.get(url)


def format_url(event):
    return (
            str(event['LI']) +
            '-' +
            event['LE'].lower().replace(' ', '-').replace('.', '') +
            '/' +
            str(event['CI']) +
            '-' +
            event['O1'].lower().replace(' ', '-').replace('.', '') +
            '-' +
            event['O2'].lower().replace(' ', '-').replace('.', '')
    )
