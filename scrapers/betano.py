import json
from scrapers.common import scrape_website
            
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
          'name': event['name'],
          'selections': []
      }
      for market in event['markets']:
        if market['name'] == 'Vencedor':
          for selection in market['selections']:
            event_data['selections'].append({
                'name': selection['name'],
                'price': selection['price']
            })
      events.append(event_data)
    return events


