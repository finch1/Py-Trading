# https://www.youtube.com/watch?v=8p240qonj0E&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&index=14

## THIS can be used to visualise open positions and suggested positions

import pandas as pd
from pandas.core.indexing import IndexSlice
import websocket, json

from sqlalchemy import create_engine
engine = create_engine('sqlite:///CryptoDB.db')

# roling 24h price from binance
# link from cloud deployed crypto bot
stream = "wss://stream.binance.com:9443/ws/!miniTicker@arr"

# start web socket stream and work with data
def on_message(ws, message):
    msg = json.loads(message)
    symbol = [x for x in msg if x['s'].endswith('USDT')]
    frame = pd.DataFrame(symbol)[['E', 's', 'c']]
    frame.E = pd.to_datetime(frame.E, unit='ms')
    frame.c = frame.c.astype(float)
    for row in range(len(frame)):
        data = frame[row:row+1]
        data[['E','c']].to_sql(data['s'].values[0], engine, index=False, if_exists='append')


# automatically populating the DB
ws = websocket.WebSocketApp(stream, on_message=on_message)
ws.run_forever()

import streamlit as st
import numpy as np
import datetime as dt

symbols = pd.read_sql('SELECT name FROM sqlite_master WHERE type="table"', engine).name.to_list()

st.title('Eyes on the goals!')

# calculating SMAs
def applytechnicals(df):
    df['SMA_7'] = df.c.rolling(7).mean() # 7 period window
    df['SMA_25'] = df.c.rolling(25).mean() # 25 period window
    df.dropna(inplace=True) # due to MA

def qry(symbol):
    now = dt.datetime.utcnow() # adjusting for different timezones
    before = now - dt.timedelta(minutes=30)
    qry_str = f"""SELECT E, c FROM '{symbol}' WHERE E >= '{before}'"""
    df = pd.read_sql(qry_str, engine)
    df.E = pd.todatetime(df.E)
    df = df.set_index('E')
    df = df.resample('1min').last()# resample data for 1 minute
    applytechnicals(df)
    df['position'] = np.where(df['SMA_7'] > df['SMA_25'], 1, 0) # checking for crossover points. not sure if this is correct
    return df

print(qry('BTCUSDT'))

def check():
    for symbol in symbols:
        if len(qry(symbol). position) > 1:
            if qry(symbol).position[-1] and qry(symbol).position.diff()[-1]:
                st.write(symbol) # write to streamlit

st.button('Get live SMA cross', on_click=check()) # execute this on streamlit                