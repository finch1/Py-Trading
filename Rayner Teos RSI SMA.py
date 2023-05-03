# https://www.youtube.com/watch?v=rYfe9Bg2GcY

import pandas as pd
import yfinance as yf
import ta 
import numpy as np

df = yf.download('TSLA', start='1996-01-01')

df['SMA200'] = ta.trend.sma_indicator(df.Close, window=200)

df['RSI'] = ta.momentum.rsi(df.Close, window=10)

df['Signal'] = np.where((df.Close > df.SMA200) & (df.RSI < 30), True, False)

Buying_dates, Selling_dates = [], []

for i in range(len(df)):
    if df.Signal.iloc[i]:
        Buying_dates.append(df.iloc[i + 1].name)
        for j in range(1, 11):
            if df['RSI'].iloc[i + j] > 40:
                Selling_dates.append(df.iloc[i + j + 1].name) # checking the next 10 days
                break
            elif j == 10:
                Selling_dates.append(df.iloc[i + j + 1].name) # checking the next 10 days

frame = pd.DataFrame({'Buying_dates': Buying_dates, 'Selling_dates':Selling_dates})
print(frame)

# checkng for the next valid date
actualtrades = frame[frame.Buying_dates > frame.Selling_dates.shift(1)]
actualtrades =frame[:1].append(actualtrades)
print(actualtrades)

profits = df.loc[actualtrades.Selling_dates].Open.values - df.loc[actualtrades.Buying_dates].Open.values

print(profits)

# calculating profits
gains = len([i for i in profits if i > 0])
total = len(profits)
print(gains/total)

# have to check how this works
relprofits = (df.loc[actualtrades.Selling_dates].Open.values - df.loc[actualtrades.Buying_dates].Open.values) / df.loc[actualtrades.Buying_dates].Open.values
print(relprofits)
print(relprofits.mean())

the video continues after 18:00


