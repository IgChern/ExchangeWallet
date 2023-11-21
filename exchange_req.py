import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
CURRENCYTOKEN = os.getenv('CURRENCYTOKEN')

import json
data_cur = 'currencies.json'
with open(data_cur, 'r') as file:
    data = json.load(file)

# Request+response
def convert(pair1, pair2):
    pair1 = pair1.upper()
    if pair1 in data.keys():
        pair2 = pair2.upper()
        if pair2 in data.keys():
            try:
                time = datetime.now().strftime("%Y-%m-%d %H:%M")
                queryurl = f'https://v6.exchangerate-api.com/v6/{CURRENCYTOKEN}/pair/{pair1}/{pair2}'
                req = requests.get(queryurl).json()
                if req['result'] == 'success':
                    rates = req['conversion_rate']
                    return f'{time}\n{pair1}/{pair2}: {round(rates, 4)}'
            except Exception as ex:
                return ex
        else:
            return f'Second currency code not found.'
    else:
            return f'First currency code not found.'




'''
# Sell price of pair
def sell_price(pair1, pair2):
    try:
        result = convert(pair1, pair2)
        lines = result.split("\n")
        sell_price = float(lines[1].split(":")[1])
        return sell_price
    except Exception as ex:
        return ex

# If input amount 
def calculate(amount, pair1, pair2):
    try:
        if str(amount).isdigit():
            amount = int(amount)
            converted = sell_price(pair1, pair2)
            return f'You will receive: {amount*converted}'
        else:
            return f'Please enter a valid amount.'
    except Exception as ex:
        return ex
'''




