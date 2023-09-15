from model.event import Event, odds_response
from data_retrievers.aggregator import get_data

events = []
odds_response = get_data()

for data in odds_response:
    events.append(Event(data))
    
arbitrage_events = []
for event in events:
    best_odds = event.find_best_odds()
    if event.arbitrage():
        arbitrage_events.append(event)
        
for event in arbitrage_events:
    event.calculate_arbitrage_bets()
    event.convert_decimal_to_american()