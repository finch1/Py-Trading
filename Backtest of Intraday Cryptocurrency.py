# https://www.youtube.com/watch?v=HB1CLz0Z1NY&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&index=12

from tqdm import tqdm
import pandas as pd
from binance.client import Client
import numpy as np
client = Client()

from sqlalchemy import create_engine

coins = ('BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'DOTUSDT', 'LUNAUSDT', 
            'AVAXUSDT', 'MATICUSDT', 'LTCUSDT', 'UNIUSDT', 'ALGOUSDT', 'TRXUSDT', 'LINKUSDT', 'MANUSDT',
            'ATOMUSDT', 'VETUSDT')

def getminutedata(symbol, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, '15m', lookback + ' days ago UTC'))
    # slice first five columns
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'O','H','L','C', 'AC']
    # some transformations
    frame[['O','H','L','C', 'AC']] = frame[['O','H','L','C', 'AC']].astype(float)
    frame.Time = pd.to_datetime(frame.Time, unit='ms')
    return frame


engine = create_engine('sqlite:///Cryptoprices.db')

# tqdm to get a progress bar for this loop
for coin in tqdm(coins):
    getminutedata(coin, '30').to_sql(coin, engine, index=False) # index=False so we use the time as index instead of an integer

# test date by reading the BTCUSDT Table
# .set_index('Time') because data is loaded with an integer index
test = pd.read_sql('BTCUSDT', engine).set_index('Time')
print(test)

def technicals(df):
    df = df.copy()
    df['return'] = np.log(df.Close.pct_change() + 1)
    df['SMA_fast'] = df.Close.rolling(7).mean()
    df['SMA_slow'] = df.Close.rolling(25).mean()
    df['postition'] = np.where(df['SMA_fast'] > df['SMA_slow'], 1, 0)
    # 1 = we have a position so multiply this by the return
    # shifting because we are entering the position after we calculate the entry
    df['strategyreturn'] = df['position'].shift(1) * df['return']
    df.dropna(inplace=True)
    return df

print(technicals(test))

print(np.exp(technicals(test)[['return', 'strategyreturn']].sum())-1)

for coin in coins:
    df = pd.read_sql(coin, engine).set_index('Time')
    print(coin)
    print(np.exp(technicals(df)[['return', 'strategyreturn']].sum()) - 1)

# takeing fees into consideration
# when position difference = 0, no position change
# when position difference = -1 or 1, there was a position change

print(technicals(test).position.diff().value_counts()) 
tot = technicals(test).position.diff().value_counts().iloc[1:].sum() # ignore the first row
print(tot * (0.075/100))

for coin in coins:
    df = pd.read_sql(coin, engine).set_index('Time')
    print(coin)
    trades = technicals(df).position.diff().value_counts().iloc[1:].sum()
    costs = trades * 0.00075
    print(np.exp(technicals(df)['return'].sum()) -1)
    print(np.exp(technicals(df)['strategyreturn'].sum()) - 1 - costs)
