# https://www.youtube.com/watch?v=vWVZxiaaTCs

from matplotlib import colors
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def strategy(df, ema1, ema2):
    df = df.copy() # do not maipulate the original set
    df['ret'] = np.log(df['Adj Close'].pct_change() + 1) # change between day and prev day
    df['EMA1'] = df['Adj Close'].ewm(span=ema1).mean()
    df['EMA2'] = df['Adj Close'].ewm(span=ema2).mean()
    df = df.dropna() # moving averages create NaN
    df['position'] = np.where(df['EMA1'] > df['EMA2'], 1, 0) # if case then 1 else 0. Function does this automatically
    # once the condition is fulfilled, buy on the next day
    df['startret'] = df['position'].shift(1) * df['ret']
    df = df.dropna()

    return df


def perfromace(df):
    return np.exp(df[['ret', 'startret']].sum()) # conter log function


df = yf.download('BTC-USD', start='2018-01-01')

perf = perfromace(strategy(df, 21, 51))
print(perf)

stratdf = strategy(df, 21, 51)

fig, ax = plt.subplots(figsize=(10,6))
ax2 = ax.twinx()
ax.plot(stratdf[['Close', 'EMA1', 'EMA2']])
ax2.plot(stratdf['position'], color = 'k')

plt.show()

## i think here we are testing different periods
# short term moving average
EMA_list1 = range(30,101,5)
# long term moving average
EMA_list2 = range(130,201,5)

profits = []
a,b = [],[]

for i,e in zip(EMA_list1, EMA_list2):
    profit = perfromace(strategy(df, i, e))
    profits.append(profit)
    a.append(i)
    b.append(e)

# create a df with the acquired data
res = pd.DataFrame(profits, [a,b]) # index , data

## the video continues with some testing automation

