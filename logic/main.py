from model.event import Event
from data_retrievers.aggregator import get_tenis_data
from data_retrievers.aggregator import get_football_data

async def run(sport):
    events = []

    match sport:
        case 'football':
            odds_response = await get_football_data()
        case 'tenis':
            odds_response = await get_tenis_data()
        case _:
            odds_response = await get_tenis_data()
    
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