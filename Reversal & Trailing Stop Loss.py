# https://www.youtube.com/watch?v=V6z1ME3-0_I&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&index=9
import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager

pair = 'ADAUSDT'
client = Client(api_key, api_secret)

engine = sqlalchemy.create_engine('sqlite:///'+pair+'stream.db')
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket(pair)

df = pd.read_sql(pair, engine)

df['Benchmark'] = df.Price.cummax() # cummax keeps track of the max cumulative value 
df['TSL'] = df.Benchmark * 0.95 # TSL = trailing stop loss
print(df)

def strategy(entry, lookback, qty, open_position=False):
    while True:
        df = pd.read_sql(pair, engine)
        lookbackperiod = df.iloc[-lookback:]
        cumret = (lookbackperiod.Price.pct_change() +1).cumprod() -1
        if cumret[cumret.last_valid_index()] < entry:
            order = client.create_order()

            print(order)
            open_position = True
            break
        # Trailing stop loss
        if open_position:
            while True:
                df = pd.read_sql(f"""SELECT * FROM {pair} WHERE Time >= '{pd.to_datetime(order['transactTime'], unit='ms')}'""", engine)
                df['Benchmark'] = df.Price.cummax()
                df['TSL'] = df.Benchmark * 0.995
                if df[df.Price < df.TSL].first_valid_index():
                    order = client.create_order()

                    print(order)
                    open_position = True                    

strategy(-0.0015,60, 50)