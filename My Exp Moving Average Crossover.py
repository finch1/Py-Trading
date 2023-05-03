# https://www.youtube.com/watch?v=8p240qonj0E

import pandas as pd
import numpy as np
import streamlit as st
import datetime as dts
import sqlalchemy
import matplotlib.pyplot as plt


# DB Connection
engine = sqlalchemy.create_engine('sqlite:///OurDataBase.db/')

# Get Symbols
prices = pd.read_sql('SELECT * FROM HistoricalData_Prices ORDER BY symbol, date', engine)
prices.date = pd.to_datetime(prices.date)
# using set()
# to remove duplicated 
# from list 
symbols = list(set(prices.symbol))

# set symbol the new index
prices.set_index('symbol', inplace=True)

st.title('Main Title')

def RSIcalc(df):
    df = df.copy()
    df['MA51'] = df['adjclose'].rolling(window=51).mean()# mean over 200 day period / last 200 days
    df['price change'] = df['adjclose'].pct_change() # Percentage change between the current and a prior element. Computes the percentage change from the immediately previous row by default. This is useful in comparing the percentage of change in a time series of elements.
    df['Upmove'] = df['price change'].apply(lambda x: x if x > 0 else 0)
    df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)
    df['avg Up'] = df['Upmove'].ewm(span=7).mean() # Provide exponential weighted (EW) functions. Available EW functions: mean(), var(), std(), corr(), cov().
    df['avg Dn'] = df['Downmove'].ewm(span=7).mean()
    df = df.dropna()
    df['RS'] = df['avg Up']/df['avg Dn']
    df['RSI'] = df['RS'].apply(lambda x : 100-(100/(x+1)))
    df.loc[(df['adjclose'] > df['MA51']) & (df['RSI'] < 30), 'Buy'] = 'Yes' # [condition , column name ] = value
    df.loc[(df['adjclose'] < df['MA51']) | (df['RSI'] > 30), 'Buy'] = 'No'
    ## print(df.head())
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

def doubleEMA(df, ema1, ema2, ema3):
    df = df.copy()
    df['ret'] = np.log(df['adjclose'].pct_change() + 1)
    df['EMA1'] = df['adjclose'].ewm(span=ema1).mean()
    df['EMA2'] = df['adjclose'].ewm(span=ema2).mean()
    df['EMA3'] = df['adjclose'].ewm(span=ema3).mean()
    df['DEMA1'] = 2 * df['EMA1'] - df['EMA1'].ewm(span=ema1).mean()
    df['DEMA2'] = 2 * df['EMA2'] - df['EMA2'].ewm(span=ema2).mean()
    df['DEMA3'] = 2 * df['EMA3'] - df['EMA3'].ewm(span=ema3).mean()
    df = df.dropna() # moving averages create NaN
    # df['position'] = np.where((df['DEMA1'] > df['DEMA2']) & (df['DEMA2'] > df['DEMA3']), 1, 0) # if case then 1 else 0. Function does this automatically

    df.loc[(df['DEMA1'] > df['DEMA2']) & (df['DEMA1'] > df['DEMA3']), 'position'] = 1 # 1 = in position
    df.loc[(df['DEMA1'] < df['DEMA2']), 'position'] = 0 # 1 = no position

    # once the condition is fulfilled, buy on the next day
    #df['startret'] = df['position'].shift(1) * df['ret'] # start calculating return after we have a position
    df = df.dropna()

    return df


def perfromace(df):
    return np.exp(df[['ret', 'startret']].sum()) # counter log function for log retruns calculated before


def TestEMAPeriods():
    ## i think here we are testing different periods
    # short term moving average
    EMA_list1 = range(30,101,5)
    # long term moving average
    EMA_list2 = range(130,201,5)

    profits = []
    a,b = [],[]

    for i,e in zip(EMA_list1, EMA_list2):
        profit = perfromace(strategy(prices, i, e))
        profits.append(profit)
        a.append(i)
        b.append(e)

    # create a df with the acquired data
    res = pd.DataFrame(profits, [a,b]) # index , data

    ## the video continues with some testing automation


# start
for symbol in symbols:

    ema1 = 7
    ema2 = 13
    ema3 = 21
    
    DoubleEmaPrices = doubleEMA(prices.loc[symbol], ema1, ema2, ema3)

    DoubleEmaPrices.set_index('date', inplace=True)
    print(DoubleEmaPrices.head())


    plt.figure(figsize=(12, 8))
    ax1 = plt.subplot(211)
    #ax1.figure.suptitle(f"Symbol: {0}",symbol, fontsize=16)

    ax1.plot(DoubleEmaPrices.index, DoubleEmaPrices['adjclose'], color='black')
    ax1.set_title("Adjusted Close Price", color='white')

    ax1.grid(True, color='#555555')
    ax1.set_axisbelow(True)
    ax1.set_facecolor('lightgray')
    #ax1.figure.set_facecolor('#121212')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax11 = ax1.twinx()
    ax11.plot(DoubleEmaPrices['position'], color='orange')
    ax11.set_ylabel('position')

    # second plot
    ax2 = plt.subplot(212, sharex=ax1) # share x axis
    ax2.plot(DoubleEmaPrices.index, DoubleEmaPrices[['DEMA1', 'DEMA2', 'DEMA3']], color='lightgray', label=['dema1', 'dema2', 'dema3'])

    ax2.set_title("Double EMA", color='white')
    ax2.grid(False, color='#555555')
    ax2.set_axisbelow(True)
    ax2.set_facecolor('black')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')


    plt.show()




    ## EMA
    # set date the new index to plot the strategy.
    start_prices.set_index(pd.DatetimeIndex(start_prices['date']), inplace=True) # datetimeindex solves the warning on plot but does not drop date column
    start_prices.drop(columns=['date'], inplace=True)
    ## print(start_prices.tail())

    ## RSI
    start_prices = RSIcalc(start_prices)
    buy, sell = getSignals(start_prices)

'''
    fig, axs = plt.subplots(2, figsize=(10,6))
    fig.suptitle('Vertically stacked subplots')

    axy0 = axs[0].twinx()
    axy1 = axs[1].twinx()

    # share the secondary axes
    axs[0].get_shared_x_axes().join( axs[1], axs[0])

    axs[0].set_title('EMA Crossover Strategy')
    axs[0].plot(start_prices[['adjclose', 'DEMA1', 'DEMA2', 'DEMA3']], label=['adjclose', ema1, ema2, ema3])
    axs[0].set_ylabel('adjclose')

    axy0.plot(start_prices['position'], color = 'k', label=symbol)
    axy0.set_ylabel('position')

    axs[1].set_title('RSI Crossover Strategy')
    axs[1].plot(start_prices[['adjclose', 'MA51']], label=['Adj', 'MA51'])
    axy1.plot(start_prices[['RSI']], color = 'g', label=['RSI'])
    axy1.axhline(y=30, color='c', linestyle='-')
    axy1.scatter(start_prices.loc[buy].index, start_prices.loc[buy]['adjclose'], marker = '^', c='g')
    axy1.scatter(start_prices.loc[buy].index, start_prices.loc[sell]['adjclose'], marker = 'v', c='r')

    axs[0].legend(loc='upper right', shadow=True)
    axy0.legend(loc='upper left', shadow=True)

    axs[1].legend(loc='upper right', shadow=True)
    axy1.legend(loc='upper left', shadow=True)

    plt.legend()
    plt.show()

    perf = perfromace(start_prices) # strategy return calculation
    print(f"{symbol} normal return {perf['ret']} Against our strategy return {perf['startret']}")

'''




