# https://www.youtube.com/watch?v=PN56q2xZ2p8&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&index=27

import pandas as pd
from tqdm import tqdm
from binance.client import Client

client = Client()
info = client.get_exchange_info()
print(info) # lists a lot of info about each symbol

# extracting symbols from returned data
symbols = [x['symbol'] for x in info['symbols']]

# total tradable coins
print(len(symbols))

exclude = ['UP', 'DOWN', 'BEAR', 'BULL']

non_lev = [symbol for symbol in symbols if all(excludes not in symbol for excludes in exclude)]
print(len(non_lev))

# assets relative to USDT
# list comprehension
relevant = [symbol for symbol in non_lev if symbol.endswith('USDT')]
print(len(relevant))

klines = {}

for symbol in relevant:
    klines[symbol] = client.get_historical_klines(symbol, '1m', '1 hour ago UTC')

# transform to DF and extracting a column
# then cast the value from string to float
# calculate the percentage change
pd.DataFrame(klines['BTCUSDT'])[4].astype(float).pct_change()

# understand the below as this is a good check
# BTC cumulative return for the last one hour
cumret = (pd.DataFrame(klines['BTCUSDT'])[4].astype(float).pct_change() +1).prod() -1

## Get returns for all Coins
returns, symbols = [],[]

for symbol in relevant:
    if len(klines[symbol]) > 0:
        cumret = (pd.DataFrame(klines[symbol])[4].astype(float).pct_change() +1).prod() -1
        returns.append(cumret)
        symbols.append(symbol)

retdf = pd.DataFrame(returns, index=symbols, columns=['ret'])