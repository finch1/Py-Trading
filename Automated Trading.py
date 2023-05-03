# https://www.youtube.com/watch?v=_IV1qfSPPwI&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&index=2

import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager

cliet = Client(api_key, api_secret)
# API Check
client.get_account()

# datastream via web socket 
# candlistick request
pd.DataFrame(client.get_historical_klines('BTCUSDT', '1m', '30 min ago UTC'))

def getminutedata(symbol, interval, loockback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, '1m', loockback + ' min ago UTC'))
    frame = frame.iloc[:,:,6] # 6 = columns
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

test = getminutedata('BTCUSDT', '1m', '30')

# buy / sell if asset


bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('BTCUSDT')