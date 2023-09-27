import websockets
import json
import uuid
import datetime
  
async def esconline_tennis_win_match_24h():
  tenis_code = 848
  data = await retrieve_info_websocket(tenis_code)
  
  content = json.loads(json.loads(data['Message'])['Requests'][0]['Content'])

  parsed_events = [event for league_item in content['LeagueDataSource']['LeagueItems'] for event in league_item['EventItems']]

  events = []

  for event in parsed_events:
    event_data = {
        'bookmaker': 'esconline',
        'name': event['EventName'].replace(':', '-'),
        'selections': [],
        'start_time': event['StartDate'],
        'start_time_ms': round(convert_time(event['StartDate']))
    }
    for market in event['MarketItems']:
      if market['MarketName'] == 'Vencedor':
        for outcome in market['OutcomeItems']:
          event_data['selections'].append({
              'name': outcome['Name'],
              'price': outcome['Odd']
          })
        break
    if len(event_data['selections']) != 2:
         continue    
    events.append(event_data)
  return events

async def esconline_football():
  football_code = 844
  data = await retrieve_info_websocket(football_code)
  
  content = json.loads(json.loads(data['Message'])['Requests'][0]['Content'])

  parsed_events = [event for league_item in content['LeagueDataSource']['LeagueItems'] for event in league_item['EventItems']]

  events = []

  for event in parsed_events:
    event_data = {
        'bookmaker': 'esconline',
        'name': event['EventName'].replace(':', '-'),
        'markets': [],
        'start_time': event['StartDate'],
        'start_time_ms': round(convert_time(event['StartDate']))
    }
    for market in event['MarketItems']:
      if market['BetType'] == 'P1XP2':
        market_data = {
          'name': 'h2h',
          'selections': []
        }

        for outcome in market['OutcomeItems']:
          market_data['selections'].append({
              'name': outcome['Name'],
              'price': outcome['Odd']
          })
        
        if len(market_data['selections']) != 3:
          continue  

        event_data['markets'].append(market_data)

      if market['BetType'] == 'total-OverUnder':   
        
        if market['Base'] == 1.5:
            market_data_3_5 = create_market(market, 1.5)
            event_data['markets'].append(market_data_3_5)
            continue
        if market['Base'] == 2.5:
            market_data_3_5 = create_market(market, 2.5)
            event_data['markets'].append(market_data_3_5)
            continue
        if market['Base'] == 3.5:
            market_data_3_5 = create_market(market, 3.5)
            event_data['markets'].append(market_data_3_5)
            continue

      if market['BetType'] == '1X12X2':
        h2h_market = find_market_by_id(event_data['markets'], 'h2h')

        if h2h_market is None:
            continue

        market_data = {
            'name': '1x 2',
            'selections': [
                {
                    'name': h2h_market['selections'][0]['name'] + ' ou empate',
                    'price': float(market['OutcomeItems'][0]['Odd'])
                },
                {
                    'name': h2h_market['selections'][2]['name'],
                    'price': h2h_market['selections'][2]['price']
                }
            ]
        }

        market_data2 = {
            'name': '1 x2',
            'selections': [
                {
                    'name': h2h_market['selections'][0]['name'],
                    'price': h2h_market['selections'][0]['price']
                },
                {
                    'name': h2h_market['selections'][2]['name'] + ' ou empate',
                    'price': float(market['OutcomeItems'][2]['Odd'])
                }
            ]
        }

        market_data3 = {
            'name': '12 x',
            'selections': [
                {
                    'name': h2h_market['selections'][0]['name'] + " ou " + h2h_market['selections'][2]['name'],
                    'price': float(market['OutcomeItems'][1]['Odd'])
                },
                {
                    'name': h2h_market['selections'][1]['name'],
                    'price': h2h_market['selections'][1]['price']
                }
            
            ]
        }

        event_data['markets'].append(market_data)
        event_data['markets'].append(market_data2)
        event_data['markets'].append(market_data3)

    if len(event_data['markets']) < 1:
         continue  
    events.append(event_data)
  return events

async def retrieve_info_websocket(sport_id):
  ws = await websockets.connect("wss://wss.estorilsolcasinos.pt/", max_size=5000000)

  init_message = json.dumps({
     "Id": generate_str_uuid(),
     "TTL": 10,
     "MessageType": 1,
     "Message": "{\"NodeType\":1,\"Identity\":\"" + generate_str_uuid() + "\",\"EncryptionKey\":\"\",\"ClientInformations\":{\"AppName\":\"Front;Registration-Origin: default\",\"ClientType\":\"Responsive\",\"Version\":\"1.0.0\",\"UserAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36\",\"LanguageCode\":\"pt\",\"RoomDomainName\":\"ESTORIL-CASINO\"}}"
  })
  
  await ws.send(init_message)

  init_response = await ws.recv()
  data = json.loads(init_response)

  req_uuid = generate_str_uuid()

  tenis_req_message = json.dumps({
     "Id": req_uuid,
     "TTL": 10,
     "MessageType": 1000,
     "Message": "{\"Direction\":1,\"Id\":\"" + generate_str_uuid() + "\",\"Requests\":[{\"Id\":\"" + generate_str_uuid() + "\",\"Type\":201,\"Identifier\":\"GetLeaguesDataSourceFromCache\",\"AuthRequired\":false,\"Content\":\"{\\\"Entity\\\":{\\\"Language\\\":\\\"pt\\\",\\\"BettingActivity\\\":0,\\\"PageNumber\\\":0,\\\"OnlyShowcaseMarket\\\":true,\\\"IncludeSportList\\\":true,\\\"EventSkip\\\":0,\\\"EventTake\\\":1000,\\\"EventType\\\":0,\\\"PlayerFavoritesLeagueIds\\\":[],\\\"SportId\\\":" + str(sport_id) + ",\\\"PeriodicFilter\\\":-1}}\"}],\"Groups\":[]}"
  })

  await ws.send(tenis_req_message)

  while data["Id"] != req_uuid:
    data = await ws.recv()
    data = json.loads(data)

  await ws.close()
  return data

def generate_str_uuid():
  return str(uuid.uuid4())


def convert_time(isoFormat):
    dt = datetime.datetime.fromisoformat(isoFormat)
    return(dt.timestamp()*1000)

def find_market_by_id(markets, id): 
    found = [market for market in markets if market['name'] == id]
    return found[0] if len(found) == 1 else None

def create_market(market, handicap):    
    market_data = {
        'name': 'total_goals_' + str(handicap),
        'selections': []
    }
    
    for outcome in market['OutcomeItems']:
          market_data['selections'].append({
              'name': outcome['Name'] + ' ' + str(outcome['Base']),
              'price': outcome['Odd']
          })

    if len((market_data['selections'])) != 2:
        return None
    
    return market_data