# Imports
import requests
import datetime
from bs4 import BeautifulSoup
import gspread
import re

def request():
    """
    Makes a GET request to the Overtek homepage and parses it using BeautifulSoup, 
    returning a list of items with class 'four columns'. 
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = 'https://www.overtek.co.uk/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    pattern = re.compile(r'four columns')
    items = soup.find_all(class_ = pattern)
    return items

def parse(items):
    """
    Takes a list of BeautifulSoup items and parses out the date, name and price.
    Returns a list of dictionaries with the parsed data.
    """
    products = []

    for item in items:
        date = datetime.datetime.now()
        name = item.find('h3').text.strip()
        price = item.find('h4').text.strip()

        # Store data in a dictionary
        item_data = {
            'Date': date,
            'Name': name,
            'Price': price
        }
        products.append(item_data)

    return products

def output(products):
    """
    Opens a Google Sheets spreadsheet and appends the scraped data to the sheet.
    
    Args:
        products (list): A list of dictionaries containing the scraped data.
    """
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('GSheetPythonScraper').sheet1

    for item in products:
        sh.append_row([str(item['Date']), str(item['Name']), str(item['Price'])])

# --- Main Execution ---
data = request()
product = parse(data)
output(product)