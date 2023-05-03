# https://www.youtube.com/watch?v=cwEORaERl2o

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

df = yf.download('TSLA', start='2020-01-01')

df['MA20'] = df['Adj Close'].ewm(span=14).mean()
df['MA50'] = df['Adj Close'].ewm(span=36).mean()

df = df.dropna()
# column slicing
df = df[['Adj Close', 'MA20', 'MA50']]

# check now and compare with the day before to identify crossing
# most times this is not a good enough trigger by itself
Buy = []
Sell = []
for i in range(len(df)):
    if df.MA20.iloc[i] > df.MA50.iloc[i] and df.MA20.iloc[i-1] < df.MA50.iloc[i-1]:
        Buy.append(i)
    elif df.MA20.iloc[i] < df.MA50.iloc[i] and df.MA20.iloc[i-1] > df.MA50.iloc[i-1]:
        Sell.append(i)

plt.figure(figsize=(12,5))
plt.plot(df['Adj Close'], label = 'Asset price', c = 'k', alpha = 0.5)
plt.plot(df['MA20'], label = 'MA20', c = 'magenta', alpha = 0.9)
plt.plot(df['MA50'], label = 'MA50', c = 'blue', alpha = 0.9)
plt.scatter(df.iloc[Buy].index, df.iloc[Buy]['Adj Close'], marker='^', color = 'g', s=100) # s = size
plt.scatter(df.iloc[Sell].index, df.iloc[Sell]['Adj Close'], marker='v', color = 'r', s=100)
plt.legend()
plt.show()


