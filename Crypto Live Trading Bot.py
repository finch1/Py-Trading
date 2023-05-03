# https://www.youtube.com/watch?v=rc_Y6rdBqXM&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&start_radio=1&rv=rc_Y6rdBqXM&t=0

import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager

cliet = Client(api_key, api_secret)
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('BTCUSDT')

def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(pd.Time, unit='ms')
    return df

createframe(msg)


engine = sqlalchemy.create_engine('sqlite:///OurDatabase.db')

while True:
    await socket.__aenter__()
    msg = await socket.recv()
    print(msg)
    frame = createframe(msg)
    frame.to_sql('BTCUSDT', engine, if_exists='append', index = False)
    print(frame)

df = pd.read_sql('BTCUSDT', engine)
df.Price.plot()

# Trendfollowing
# if the crypto was rising by x% -> Buy
# exit when profit is above 0.15% or loss is crossing -0.15%

def strategy(entry, lookback, qty, open_position=False):# lookback = how many rows to use to calculate 
    while True:
        df = pd.read_sql('BTCUSDT', engine) # request live data
        lookbackperiod = df.iloc[-lookback:] # filter until time period in seconds
        cumret = (lookbackperiod.Price.pct_change() +1).cumprod() -1
        if not open_position:
            if cumret[cumret.last_valid_index()] > entry:
                order = client.create_order(symbol='BTCUSDT',
                                            side='BUY', 
                                            type='MARKET', 
                                            quantity=qty)# create order

                print(order) # save order to DB idealy
                open_position = True
                break
        if open_position:
            while True:
                df = pd.read_sql('BTCUSDT', engine)
                sincebuy = df.loc[df.Time > pd.to_datetime(order['transactTime'], unit='ms')]

                if len(sincebuy) > 1: # if not empty frame
                    sincebuyret = (sincebuy.Price.pct_change() +1).cumprod() -1 # return since asset was purchased. 
                    last_entry = sincebuyret[sincebuyret.last_valid_index()]
                    if last_entry > 0.0015 or last_entry < -0.015:
                        order = client.create_order(symbol='BTCUSDT',
                                            side='SELL', 
                                            type='MARKET', 
                                            quantity=qty)# create order
                    print(order) # save order to DB idealy
                    break



