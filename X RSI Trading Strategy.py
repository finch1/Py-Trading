# https://www.youtube.com/watch?v=pB8eJwg7LJU&t=1809s 
'''
Buy decision if: 10-period RSI of the stock is below 30
Sell decision if: 10-period RSI is above 40 OR after 10 trading days

Step 1: Calculating up and down moves

upmoves:    take the daily return if return is positive
            take 0 if daily return is negative or zero

downmoves:  absolute value of daily return if return is negative
            zero if return is positive or zero

Step 2: Average Upmoves and Downmoves - Pick an average method -e.g. Exp moving average 

Step 3: RS and RSI calculation
1. RS -> Average Upmove / Average Downmove
2. RSI -> 100 - 100/(1+RS)
'''


import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


pd.options.mode.chained_assignment = None # disables some sort of warnings


def RSIcalc(asset):
    print(asset)
    df = yf.download(asset, start='2011-01-01')
    df['MA51'] = df['Adj Close'].rolling(window=51).mean()# mean over 200 day period / last 200 days
    df['price change'] = df['Adj Close'].pct_change() # Percentage change between the current and a prior element. Computes the percentage change from the immediately previous row by default. This is useful in comparing the percentage of change in a time series of elements.
    df['Upmove'] = df['price change'].apply(lambda x: x if x > 0 else 0)
    df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)
    df['avg Up'] = df['Upmove'].ewm(span=14).mean() # Provide exponential weighted (EW) functions. Available EW functions: mean(), var(), std(), corr(), cov().
    df['avg Dn'] = df['Downmove'].ewm(span=14).mean()
    df = df.dropna()
    df['RS'] = df['avg Up']/df['avg Dn']
    df['RSI'] = df['RS'].apply(lambda x : 100-(100/(x+1)))
    df.loc[(df['Adj Close'] > df['MA51']) & (df['RSI'] < 30), 'Buy'] = 'Yes'
    df.loc[(df['Adj Close'] < df['MA51']) | (df['RSI'] > 30), 'Buy'] = 'No'
    return df

def getSignals(df):
    Buying_dates = []
    Selling_dates = []

    for i in range(len(df)):
        if "Yes" in df['Buy'].iloc[i]:
            Buying_dates.append(df.iloc[i].name)
            for j in range(1,11):
                if df['RSI'].iloc[i+j] > 40:
                    Selling_dates.append(df.iloc[i+j].name)
                    break
                elif j == 10:
                    Selling_dates.append(df.iloc[i+j].name)
    return Buying_dates, Selling_dates

tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S&P_500_companies")[0]
# extract first column
symbols = tickers.Symbol.to_list()
# replacing characters in ticker
symbols = [i.replace('.','-') for i in symbols]

frame = RSIcalc(symbols[0])
print(frame[['Adj Close','price change','Upmove','Downmove','avg Up','avg Dn','RS','RSI','Buy']])

buy, sell = getSignals(frame)
plt.figure(figsize=(12,5))
plt.scatter(frame.loc[buy].index, frame.loc[buy]['Adj Close'], marker = '^', c='g')
plt.plot(frame['Adj Close'], alpha=0.7)

plt.show()

# calculate profits
profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values

# calculate wins
wins = [i for i in profits if i > 0]
print(len(wins)/len(profits))

# The video continues