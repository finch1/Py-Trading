# https://www.youtube.com/watch?v=lNvJXKXUQ_U&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&index=6

'''
Overall Strategy

Buy when MACD diff ( Difference between MACD and Signal line) is crossing above 0
Sell when MACD diff is crossing below 0

'''

from binance.client import Client
import pandas as pd
import ta
from time import sleep # to cover for timeout error
client = Client(api_key, api_secret)

def getminutedata(symbol):
    try:
        df = pd.DataFrame(client.get_historical_klines(symbol, '1m', '40m UTC'))
    except BinanceAPIException as e:
        print(e)
        sleep(60)
        df = pd.DataFrame(client.get_historical_klines(symbol, '1m', '40m UTC'))
    # data cleaning
    # filtering the first 6 columns
    df = df.iloc[:,:6] 
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df.set_index('Time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.astype(float)
    return df


def tradingstrat(symbol, qty, open_position = False):
    # start wit false position then true if meets strategy
    # continous loop
    while True:
        df = getminutedata(symbol)
        if not open_position:
            if ta.trend.macd_diff(df.Close).iloc[-1] > 0 and ta.trend.macd_diff(df.Close).iloc[-2] < 0:
                order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quantity=qty)
                print(order)
                open_position = True
                # record our position
                buyprice = float(order['fills'][0]['price'])
                break # stop while loop cause we have a positionand do not require buying any more
    
    if open_position:
        while True:
            df = getminutedata(symbol)
            if ta.trend.macd_diff(df.Close).iloc[-1] < 0 and ta.trend.macd_diff(df.Close).iloc[-2] > 0:
                order = client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=qty)
                print(order)
                open_position = False
                # record our position
                sellprice = float(order['fills'][0]['price'])
                print(f'profit = {(sellprice - buyprice)/buyprice}')
                break # stop while loop cause we have a no positionand do require buying again

## loop to run multiple times
tradingstrat('ETHUSDT', qty=0.1)