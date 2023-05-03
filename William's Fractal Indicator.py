# https://www.youtube.com/watch?v=4MnNft7Squk

import yfinance as yf
import pandas as pd
import numpy as np

import ta

df = yf.download('TSLA', start = '2021-11-22', interval = '15m')

df['EMA200'] = ta.trend.ema_indicator(df.Close, window=200)

# calculating william's fractal indicator
# finding the high value 
# center = 4 previous days and 4 subsequent days
df['wf_Top_bool'] = np.where(df['High'] == df['High'].High.rolling(9, center=True).max(), True, False)

# to calculate trend, compare gradients of last two highs and last two lows

df['wf_Top'] = np.where(df['High'] == df['High'].High.rolling(9, center=True).max(), df['High'], None) # ,if true, if false

df['wf_Top'] = df['wf_Top'].ffill() # drags the same value to subsequent rows

df.dropna(inplace=True)

# if close crosses above the fractal high
df['Buy'] = np.where((df.Close > df.wf_Top) & (df.Close > df.EMA200), 1, 0)

df['SL'] = np.where(df.Buy == 1, df.Close - (df.Close - df.Low), 0)
df['TP'] = np.where(df.Buy == 1, df.Close + (df.Close - df.Low) * 1.5, 0)

buys, sell = [], []

for i in range(len(df)):
    if df.Buy.iloc[i]:
        buys.append(df.iloc[i].name)
        for j in range(len(df) - i):
            if df.TP.iloc[i] < df.Clsoe.iloc[i + j] or df.SL.iloc[i] > df.Close.iloc[i + j]:
                sell.append(df.iloc[i + j].name)
                #break on sale
                break

frame = pd.DataFrame([buys, sell].T.dropna)
# getting rid of double buy entries
frame.columns = ['Buys', 'Sells']
actualtrades = frame[frame.Buys > frame.Sells.shift(1)]

