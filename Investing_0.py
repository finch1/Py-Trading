## https://www.youtube.com/watch?v=xfzGZB4HhEE&t=2200s
import numpy as np # numpy is inherently fast
import pandas as pd
import requests
import xlsxwriter # read write to excel
import math

def chunks(lst, n):
    # Yield successive n-sized chunks from list
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

        
# import ticker symbols
stocks = pd.read_csv("Investing_0_sp_500_stocks.csv")

# acquiring an API token. Requries autentication
from secrets import IEX_CLOUD_API_TOKEN

# make an API call for market cap for each stock and price of each stock
symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url)

if data.status_code != 200:
    print("URL ERROR")

data = data.json()

# access value by key in dictionary
print(data['symbol'])

# parsing our api call
price = data['latestPrice']
market_cap = data['marketCap']

my_columns = ['Ticker', 'Stock Price', 'Market Cap', 'Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns=my_columns)

# Looping through the ticker in our list of stocks
for symbol in stocks['Ticker'][:5]:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url)
    if data.status_code != 200:
        print("URL ERROR")

    data = data.json()

    # append does not modify the dataframe
    final_dataframe = final_dataframe.append(
        pd.Series(
            [
                symbol,
                data['latestPrice'],
                data['marketCap'],
                'N/A'
            ],
            index=my_columns
        ),
        ignore_index=True
    )

