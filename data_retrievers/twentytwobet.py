import requests
import json
import datetime

blacklisted_outcome1 = ['Home (Apostas especiais)', 'Equipa da Casa']
blacklisted_outcome2 = ['Convidados (especial)', 'Equipa visitante']

blacklisted_comp_ids = [2150631, 2590430, 2390706, 2322382, 2498900]


def twentytwobet_tennis_win_match():
    comps_ids = get_competition_ids('tennis')

    result_events = get_events_from_competitions(comps_ids, 'tennis')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': '22bet',
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S'] * 1000
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
    # only retrieves 50 events and no pagination
    # result = requests.get(
    #    "https://22win88.com/LineFeed/Get1x2_VZip?sports=1&count=300&lng=pt&tf=3000000&tz=1&mode=4&country=148"
    #    "&partner=151&getEmpty=true")

    # resultDict = json.loads(result.content)

    comps_ids = get_competition_ids('football')

    result_events = get_events_from_competitions(comps_ids, 'football')

    events = []
    for event in result_events:
        event_data = {
            'bookmaker': '22bet',
            'name': event['O1'] + ' - ' + event['O2'],
            'markets': [],
            'start_time': str(convert_time(event['S'])),
            'start_time_ms': event['S'] * 1000
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
            'name': 'Acima de 1.5',
            'price': float(selections_1_5[0]['C'])
        }))

        market_data_1_5['selections'].insert(1, ({
            'name': 'Abaixo de 1.5',
            'price': float(selections_1_5[1]['C'])
        }))

        markets.append(market_data_1_5)

    if len(selections_2_5) == 2:
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

    if len(selections_3_5) == 2:
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
                'name': event['O1'] + " ou Empate",
                'price': float(selection['C'])
            }))

            market_data_1x_2['selections'].insert(1, ({
                'name': event['O2'],
                'price': float(h2h_market['selections'][2]['price'])
            }))

        elif selection['T'] == 5:
            market_data_12_x = {
                'name': '12 x',
                'selections': []
            }

            market_data_12_x['selections'].insert(0, ({
                'name': event['O1'] + " ou " + event['O2'],
                'price': float(selection['C'])
            }))

            market_data_12_x['selections'].insert(1, ({
                'name': "Empate",
                'price': float(h2h_market['selections'][1]['price'])
            }))

        elif selection['T'] == 6:

            market_data_1_2x = {
                'name': '1 2x',
                'selections': []
            }

            market_data_1_2x['selections'].insert(0, ({
                'name': event['O1'],
                'price': float(h2h_market['selections'][0]['price'])
            }))

            market_data_1_2x['selections'].insert(1, ({
                'name': event['O2'] + " ou Empate",
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


def get_competition_ids(sport):
    sport_id = 1
    sport_name = 'Football'

    if sport == 'football':
        sport_id = 1
        sport_name = 'Football'
    elif sport == 'tennis':
        sport_id = 4
        sport_name = 'Tennis'

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
    for comp in comps:
        # if number of games in comp is higher than 15, consider relevant to request

        if comp['LI'] in blacklisted_comp_ids:
            continue

        number_of_games += comp['GC']

        if number_of_games >= 50:
            ids.sort()
            grouped_ids.append(ids)
            ids = []
            number_of_games = 0
        else:
            ids.append(comp['LI'])

    return grouped_ids


def get_events_from_competitions(competition_ids, sport):
    if sport == 'football':
        sport_id = 1
    elif sport == 'tennis':
        sport_id = 4

    url_template = ("https://22win88.com/LineFeed/Get1x2_VZip?sports={sport_id}&champs={"
                    "competition_id}&count=50&lng=pt&tf=2880&tz=1&mode=4&country=148&partner=151&getEmpty=true")
    events = []

    for ids in competition_ids:
        url = url_template.format(url_template, sport_id=sport_id, competition_id=','.join(map(str, ids)))
        result = requests.get(url)
        result_dict = json.loads(result.content)

        events.extend(result_dict['Value'])

    return events
