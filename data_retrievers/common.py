import json

import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service


def scrape_website(url):
    # Specify the path to geckodriver if not in PATH
    geckodriver_path = '/usr/local/bin/geckodriver'  # or the path where you placed geckodriver
    service = Service(geckodriver_path)

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Run in headless mode

    # Initialize the Firefox WebDriver
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(url)

    # Get the page source or content
    content = driver.page_source

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Find the script tag containing the JSON data (customize the selector as needed)
    # For example, if the JSON is inside a <script> tag with a specific id or class
    main_data = json.loads(soup.find('div', id='json').getText())

    driver.quit()

    return main_data


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
