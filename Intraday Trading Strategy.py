# https://www.youtube.com/watch?v=BhOdgrxWi5c&t=424s

'''
Buying Condition : if the return after two hours breaks a certain threshold ( e.g. +2%) buy the asset
Selling Condition : The asset drops until a certain threshold OR the asset climbs until this threshold
'''

from numpy import busday_count
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None # disables some sort of warnings

asset = 'TSLA'
intraday = yf.download(asset, start='2021-12-17', end = '2021-12-24', interval= '5m')
print(intraday.shape)
print(intraday.iloc[0].Open)

def Intradaytrend(df, entry, exit):
    ret_120min = df.iloc[120].Open/df.iloc[0].Open - 1  # minus one may be wrong
    tickret = df.Open.pct_change()
    if ret_120min > entry:
        buyprice = df.iloc[121].Open
        buytime = df.iloc[121].name
        cumulated = (tickret.loc[buytime:] + 1).cumprod() - 1
        exittime = cumulated[(cumulated < - exit) | (cumulated > exit)].first_valid_index()
        # if no movement was detected
        if exittime == None:
            exitprice = df.iloc[-1].Open
        else:
            exitprice = df.loc[exittime + dt.timedelta(minutes=5)].Open
            profit = exitprice - buyprice
            profitrel = profit/buyprice
            return profitrel
    else: return None


profit = Intradaytrend(intraday, 0.01, 0.01)
print(profit)

## BACKTEST
frames = []
datesframe = yf.download(asset, start='2021-12-01', end='2021-12-24')

for i in datesframe.index:
    frames.append(yf.download(asset, start=i, end=i+dt.timedelta(days=1), interval='5m')) 

returns = []

for i in frames:
    returns.append(Intradaytrend(i, 0.01, 0.01))

for r in returns:
    print(r)