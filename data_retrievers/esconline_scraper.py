import websockets
import json
  
async def esconline_tennis_win_match_24h():
  ws = await websockets.connect("wss://wss.estorilsolcasinos.pt/")
  init_message = json.dumps({
     "Id": "f058ea95-51ee-8efa-33db-f4baf4efe87e",
     "TTL": 10,
     "MessageType": 1,
     "Message": "{\"NodeType\":1,\"Identity\":\"fb5f1df0-dc5b-43ec-b09c-eefae9ae4f3b\",\"EncryptionKey\":\"\",\"ClientInformations\":{\"AppName\":\"Front;Registration-Origin: default\",\"ClientType\":\"Responsive\",\"Version\":\"1.0.0\",\"UserAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36\",\"LanguageCode\":\"pt\",\"RoomDomainName\":\"ESTORIL-CASINO\"}}"
  })
  
  await ws.send(init_message)

  init_response = await ws.recv()
  data = json.loads(init_response)

  tenis_req_message = json.dumps({
     "Id": "cba7302a-4e92-7431-be7b-e8d014a70c2a",
     "TTL": 10,
     "MessageType": 1000,
     "Message": "{\"Direction\":1,\"Id\":\"f05b5d98-8683-b9d4-c9b3-416c4d57edbe\",\"Requests\":[{\"Id\":\"6f7a66e1-837c-5386-90c4-a1527a8c2d22\",\"Type\":201,\"Identifier\":\"GetLeaguesDataSourceFromCache\",\"AuthRequired\":false,\"Content\":\"{\\\"Entity\\\":{\\\"Language\\\":\\\"pt\\\",\\\"BettingActivity\\\":0,\\\"PageNumber\\\":0,\\\"OnlyShowcaseMarket\\\":true,\\\"IncludeSportList\\\":true,\\\"EventSkip\\\":0,\\\"EventTake\\\":1000,\\\"EventType\\\":0,\\\"PlayerFavoritesLeagueIds\\\":[],\\\"SportId\\\":848,\\\"PeriodicFilter\\\":-1}}\"}],\"Groups\":[]}"
  })

  await ws.send(tenis_req_message)

  while data["Id"] != "cba7302a-4e92-7431-be7b-e8d014a70c2a":
    data = await ws.recv()
    data = json.loads(data)

  await ws.close()
  
  content = json.loads(json.loads(data['Message'])['Requests'][0]['Content'])

  parsed_events = [event for league_item in content['LeagueDataSource']['LeagueItems'] for event in league_item['EventItems']]

  events = []

  for event in parsed_events:
    event_data = {
        'bookmaker': 'esconline',
        'name': event['EventName'],
        'selections': []
    }
    for market in event['MarketItems']:
      if market['MarketName'] == 'Vencedor':
        for outcome in market['OutcomeItems']:
          event_data['selections'].append({
              'name': outcome['Name'],
              'price': outcome['Odd']
          })
        break
    events.append(event_data)
  return events
