# https://www.youtube.com/watch?v=nQkaJ207xYI&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&index=3
'''
Technical indicator: ROC(rate of change)
ROC(t) = Close(t) / Close(t-n)*100

Strategy overall
Buy when ROC (last 30 ticks or almost 30 seconds) is crossing above 0
Sell if we made 0.02% profit or a 99.5% trailing stop loss
'''

import websockets
import json
import pandas as pd
import asyncio
from binance.client import Client
import ta # technical analysis

client = Client(api_key, api_secret)
stream = websockets.connect('wss://stream.binance.com:9443/streams?=adausdt@miniTicker')

# PARAMETERS
# get data
# our position, initially false
df = pd.DataFrame()
open_position = False

def createframe(msg):
    df = pd.Dataframe([msg])
    df = df.loc[:, ['s', 'E', 'c']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df



async def main():
    async with stream as receiver:
        while True: # stream data requests
            data = await receiver.recv()
            data = json.loads(data)['data'] # extract dict called data to get the info we need
            print(data)
            ## df = createframe(data) # one time visualise
            ## print(df)
            df = df.append(createframe(data))
            if len(df) > 30: # to check 30 data point, we must first have 30 data points
                if not open_position: # if we hold no assets
                    if ta.momentum.roc(df.Price, 30).iloc[-1] > 0 and \
                        ta.momentum.roc(df.Price, 30).iloc[-2]:
                        order = client.create_order(symbol='BTCUSDT',
                                                side='BUY', 
                                                type='MARKET', 
                                                quantity=qty)# create order
                        print(order)
                        open_position = True
                        buyprice = float(order['fills'][0]['price'])
                if open_position: # get price after order to set stop loss
                    subdf = df[df.Time >= pd.to_datetime(order['transactTime'], unit='ms')]
                    if len(subdf) > 1:
                        subdf['highest'] = subdf.Price.cummax()
                        subdf['trailingstop'] = subdf['highest'] * 0.995
                        if subdf.iloc[-1].Price < subdf.iloc[-1].trailingstop or \
                            df.iloc[-1].Price / float(order['fills'][0]['price']) > 1.002:
                            order = client.create_order(symbol='BTCUSDT',
                                                side='SELL', 
                                                type='MARKET', 
                                                quantity=qty)# create order
                            print(order)
                            sellprice = float(order['fills'][0]['price'])# profit
                            print(f"You made {(sellprice - buyprice)/buyprice} profit")
                            open_position = False

                print(df.iloc[-1])



           

# to run as executable
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
