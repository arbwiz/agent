from data_retrievers.common import scrape_website
import re
            
def betclic_tennis_win_match_24h():
  url = 'https://www.betclic.pt/tenis-s2'
  soup = scrape_website(url)

  
  #odd = soup.find_all("sports-events-event", {"class": "groupEvents_card ng-star-inserted"})[0].find_all("sports-markets-default-v2", {"class": "market ng-star-inserted"})[0].find_all("sports-selections-selection")[0].find_all("span")[2].string
  #name = soup.find_all("sports-events-event", {"class": "groupEvents_card ng-star-inserted"})[0].find_all("sports-markets-default-v2", {"class": "market ng-star-inserted"})[0].find_all("sports-selections-selection")[0].find_all("span")[0].find_all("span")[0].string
  
  events = []
  for event in soup.find_all("sports-events-event", {"class": "groupEvents_card ng-star-inserted"}):
    event_data = {
        'name': '',
        'selections': []
    }
    event_name = ''

    for market in event.find_all("sports-markets-default-v2", {"class": "market ng-star-inserted"}):
        for selection in market.find_all("sports-selections-selection"):

          names = ""

          for partial_name in selection.find_all("span")[0].find_all("span"):
             names += partial_name.string

          name = names.replace("\xa0", " ")
          oddStr = selection.find_all("span")[2].string if len(selection.find_all("span")) <= 5 else selection.find_all("span")[3].string
          odd = float(oddStr.replace(",", ".")) if oddStr != '-' else 1
          event_data['selections'].append({
              'name': name,
              'price': odd
          })
        event_name = event_data['selections'][0]['name'] + " - " + event_data['selections'][1]['name']
    event_data["name"] = event_name
    
    events.append(event_data)
  return events


