import requests
import json
import datetime

from data_retrievers.common import is_valid_tennis_event, is_valid_football_event, is_valid_basket_event
from utils import sanitize_text


async def lebull_tennis():
    # might change
    tenant_header = "126dc7bf-288b-4f72-9536-3aa54648c0f4"
    url = "https://sportsbook-betting-prod.gtdevteam.work/sports/3/leagues/upcoming?leagueTimeFilter=10&languageId=14&stakeTypes=%5B1%2C%2080%2C%20356%2C%20702%2C%20176415%2C%20183254%2C%20217797%2C%20357318%2C%202%2C%203%2C%2026%2C%2037%2C%20545%2C%20144%2C%20724%2C%20274556%2C%20313638%2C%20313639%5D&isStakeGrouped=true&timeZone=1&checkIsActive=true&setParameterOrder=false&getMainMatch=false"

    headers = {'X-Auth-Tenant-Id': tenant_header}
    response = requests.get(url, headers=headers)

    res_dict = json.loads(response.content)

    lebull_events = [event for league in res_dict for event in league['games']]

    events = []
    for event in lebull_events:
        if event['isLive'] == 'true':
            continue
        event_data = {
            'bookmaker': 'lebull',
            'competition': event['leagueName'],
            'name': event['teamA'] + ' - ' + event['teamB'],
            'participant_a': sanitize_text(event['teamA']),
            'participant_b': sanitize_text(event['teamB']),
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time(event['timestamp'])),
            'start_time_ms': event['timestamp'],
            'url': 'https://www.lebull.pt/pt/sportsbook?page=/event/{event_id}?isLive=false'.format(
                event_id=str(event['eventId']))
        }

        for stakeType in event['stakeTypes']:
            if stakeType['stakeTypeName'] == 'Vencedor':
                for selection in stakeType['stakes']:
                    event_data['markets'][0]['selections'].append({
                        'name': selection['stakeName'],
                        'price': float(selection['betFactor'])
                    })

        if is_valid_tennis_event(event_data):
            events.append(event_data)
    return events


async def lebull_basket():
    # might change
    tenant_header = "126dc7bf-288b-4f72-9536-3aa54648c0f4"
    url = "https://sportsbook-betting-prod.gtdevteam.work/sports/4/leagues/upcoming?languageId=14&isStakeGrouped=true&timeZone=1&checkIsActive=true&setParameterOrder=false&leagueTimeFilter=10&getMainMatch=false"

    headers = {'X-Auth-Tenant-Id': tenant_header}
    response = requests.get(url, headers=headers)

    res_dict = json.loads(response.content)

    lebull_events = [event for league in res_dict for event in league['games']]

    events = []
    for event in lebull_events:
        if event['isLive'] == 'true':
            continue

        participant_a = sanitize_text(event['teamA'])
        participant_b = sanitize_text(event['teamB'])

        if event['leagueName'] == 'NBA':
            participant_a = sanitize_text(event['teamB'])
            participant_b = sanitize_text(event['teamA'])

        event_data = {
            'bookmaker': 'lebull',
            'competition': event['leagueName'],
            'name': event['teamB'] + ' - ' + event['teamA'],
            'participant_a': participant_a,
            'participant_b': participant_b,
            'markets': [{
                'name': 'h2h',
                'selections': []
            }],
            'start_time': str(convert_time(event['timestamp'])),
            'start_time_ms': event['timestamp'],
            'url': 'https://www.lebull.pt/pt/sportsbook?page=/event/{event_id}?isLive=false'.format(
                event_id=str(event['eventId']))
        }

        for stakeType in event['stakeTypes']:
            if stakeType['stakeTypeName'] == 'Vencedor':
                for selection in stakeType['stakes']:
                    event_data['markets'][0]['selections'].append({
                        'name': selection['stakeName'],
                        'price': float(selection['betFactor'])
                    })

        if is_valid_basket_event(event_data):
            if event['leagueName'] == 'NBA':
                aux = event_data['markets'][0]['selections'][0]
                event_data['markets'][0]['selections'][0] = event_data['markets'][0]['selections'][1]
                event_data['markets'][0]['selections'][1] = aux
            events.append(event_data)
    return events


async def lebull_football():
    # might change
    tenant_header = "126dc7bf-288b-4f72-9536-3aa54648c0f4"
    url = "https://sportsbook-betting-prod.gtdevteam.work/sports/1/leagues/upcoming?leagueTimeFilter=10&languageId=14&stakeTypes=%5B1%2C%2080%2C%20356%2C%20702%2C%20176415%2C%20183254%2C%20217797%2C%20357318%2C%202%2C%203%2C%2026%2C%2037%2C%20545%2C%20144%2C%20724%2C%20274556%2C%20313638%2C%20313639%5D&isStakeGrouped=true&timeZone=1&checkIsActive=true&setParameterOrder=false&getMainMatch=false"

    headers = {'X-Auth-Tenant-Id': tenant_header}
    response = requests.get(url, headers=headers)

    res_dict = json.loads(response.content)

    lebull_events = [event for league in res_dict for event in league['games']]

    events = []
    for event in lebull_events:
        if event['isLive'] == 'true':
            continue
        event_data = {
            'bookmaker': 'lebull',
            'competition': event['leagueName'],
            'name': event['teamA'] + ' - ' + event['teamB'],
            'participant_a': sanitize_text(event['teamA']),
            'participant_b': sanitize_text(event['teamB']),
            'markets': [],
            'start_time': str(convert_time(event['timestamp'])),
            'start_time_ms': event['timestamp'],
            'url': 'https://www.lebull.pt/pt/sportsbook?page=/event/{event_id}?isLive=false'.format(
                event_id=str(event['eventId']))
        }

        market_data = {
            'name': 'h2h',
            'selections': []
        }

        for stakeType in event['stakeTypes']:
            if stakeType['stakeTypeName'] == '1X2':
                for selection in stakeType['stakes']:
                    market_data['selections'].append({
                        'name': selection['stakeName'],
                        'price': float(selection['betFactor'])
                    })
        if len(market_data['selections']) != 3:
            continue
        event_data['markets'] = [market_data]

        if is_valid_football_event(event_data):
            events.append(event_data)
    return events


def convert_time(millis):
    dt = datetime.datetime.fromtimestamp(millis / 1000)
    return (dt.isoformat())


def find_market_by_id(markets, id):
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None
