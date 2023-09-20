import requests
import json
import datetime

def lebull_football():
    # might change
    tenant_header = "126dc7bf-288b-4f72-9536-3aa54648c0f4"
    url = "https://sportsbook-betting-prod.gtdevteam.work/sports/1/leagues/upcoming?leagueTimeFilter=14&languageId=14&stakeTypes=%5B1%2C%2080%2C%20356%2C%20702%2C%20176415%2C%20183254%2C%20217797%2C%20357318%2C%202%2C%203%2C%2026%2C%2037%2C%20545%2C%20144%2C%20724%2C%20274556%2C%20313638%2C%20313639%5D&isStakeGrouped=true&timeZone=1&checkIsActive=true&setParameterOrder=false&getMainMatch=false"

    headers = {'X-Auth-Tenant-Id': tenant_header}
    response = requests.get(url, headers=headers)

    res_dict = json.loads(response.content)
    
    lebull_events = [event for league in res_dict for event in league['games']]

    events = []
    for event in lebull_events:
        event_data = {
            'bookmaker': 'lebull',
            'name': event['teamA'] + ' - ' + event['teamB'],
            'selections': [],
            'start_time': str(convert_time(event['timestamp'])),
            'start_time_ms': event['timestamp']
        }

        for stakeType in event['stakeTypes']:
            if stakeType['stakeTypeName'] == '1X2':
                for selection in stakeType['stakes']:
                    event_data['selections'].append({
                        'name': selection['stakeName'],
                        'price': float(selection['betFactor'])
                    })
        if len(event_data['selections']) != 3:
            continue
        events.append(event_data)
    return events
        
def convert_time(millis):
    dt = datetime.datetime.fromtimestamp(millis/1000)
    return(dt.isoformat())