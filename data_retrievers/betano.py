import json
import requests
import datetime
from data_retrievers.common import scrape_website
            
def betano_tennis_win_match_24h():
  url = 'https://www.betano.pt/sport/tenis/jogos-de-hoje/'
  soup = scrape_website(url)

  data = soup.find('body').find('script').text
  json_end = data.rfind('}')
  json_start = data.find('{')
  
  main_data=json.loads(data[json_start:json_end+1])

  events = []
  for block in main_data['data']['blocks']:
    for event in block['events']:
      event_data = {
          'bookmaker': 'betano',
          'name': event['name'],
          'selections': [],
          'start_time': str(convert_time(event['startTime'])),
          'start_time_ms': event['startTime']
      }
      for market in event['markets']:
        if market['name'] == 'Vencedor':
          for selection in market['selections']:
            event_data['selections'].append({
                'name': selection['name'],
                'price': float(selection['price'])
            })
      if len(event_data['selections']) != 2:
        continue
      events.append(event_data)
    return events

def betano_football():
  url = 'https://www.betano.pt/api/sport/futebol/jogos-de-hoje/?sort=Leagues&req=la,s,stnf,c,mb'

  result = requests.get(url)

  main_data = json.loads(result.content)

  events = []
  for block in main_data['data']['blocks']:
    for event in block['events']:
      event_data = {
          'bookmaker': 'betano',
          'name': event['name'],
          'selections': [],
          'start_time': str(convert_time(event['startTime'])),
          'start_time_ms': event['startTime']
      }
      if not event['markets']:
        break
      for market in event['markets']:
        if market['type'] == 'MRES' or market['type'] == 'MR12':
          for selection in market['selections']:
            event_data['selections'].append({
                'name': selection['fullName'],
                'price': float(selection['price'])
            })
          break
      if len(event_data['selections']) != 3:
        continue        
      events.append(event_data)
  return events

def convert_time(millis):
    dt = datetime.datetime.fromtimestamp(millis/1000)
    return(dt.isoformat())