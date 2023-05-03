# https://www.youtube.com/watch?v=8p240qonj0E

import pandas as pd
import websockets, json
from sqlalchemy import create_engine, engine

engine = create_engine('sqllite:///CryptoDB.db')

stream = "wss://stream.binance.com:9443/ws/!miniTicker@arr"

def on_message(ws, message):
    msg = json.loads(message)
    symbol = [x for x in msg if x['s'].endswith('USDT')] # filtering on USDT only
    frame = pd.DataFrame(symbol)[['E','s','c']]  # creating a dataframe with columns
    frame.E = pd.to_datetime(frame.E, unit='ms')
    frame.c =  frame.c.astype(float) # changing type to apply calculations

    for row in range(len(frame)): # for every currency 
        data = frame[row:row+1]
        data[['E', 'c']].to_sql(data['s'].values[0], engine, index=False, if_exists='append')


ws = websockets.WebsocketApp(stream, on_message=on_message)
ws.run_forever()

