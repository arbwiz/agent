import requests
from bs4 import BeautifulSoup
import time


def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def is_valid_tennis_event(event):
    if len(event['markets']) < 1:
        return False
    # event has h2h market
    if len(event['markets'][0]['selections']) != 2:
        return False

    current_time_ms = int(round(time.time() * 1000))
    # event is going live (less or equal to 5 min to start)
    if (current_time_ms + 300000) >= event['start_time_ms']:
        return False

    return True


def is_valid_football_event(event):
    if len(event['markets']) < 1:
        return False
    # event has h2h market
    if len(event['markets'][0]['selections']) != 3:
        return False

    current_time_ms = int(round(time.time() * 1000))
    # event is going live (less or equal to 5 min to start)
    if (current_time_ms + 300000) >= event['start_time_ms']:
        return False

    return True

def is_valid_basket_event(event):
    if len(event['markets']) < 1:
        return False
    # event has h2h market
    if len(event['markets'][0]['selections']) != 2:
        return False

    current_time_ms = int(round(time.time() * 1000))
    # event is going live (less or equal to 5 min to start)
    if (current_time_ms + 300000) >= event['start_time_ms']:
        return False

    return True
