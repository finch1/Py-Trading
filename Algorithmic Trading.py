# https://www.youtube.com/watch?v=XK2IU5vRJr0&list=PLwEOixRFAUxZmM26EYI1uYtJG39HDW1zm&index=2

import pandas as pd
df = pd.read_csv("")
df.tail()

import numpy as np
import pandas_ta as ta

df['ATR'] = df.ta.atr(length=20) # taking into account the last 20 bars
df['RSI'] = df.ta.rsi()
df['Average'] = df.ta.midprice(length=1) # midprice
df['MA40'] = df.ta.sma(length=40) # 40 bars
df['MA80'] = df.ta.sma(length=80) # 80 bars
df['MA160'] = df.ta.sma(length=160) # 160 bars. least sensitive


from scipy.stats import linregress
# calculate gradient
def get_slope(array):
    y = np.array(array)
    x = np.arange(len(y))
    slope, intercept, r_value, p_value, std_err = linregress(x,y)
    return slope

backrollingN = 6

## GET THE Complete code as it does not show in the video
# https://drive.google.com/file/d/1JTm6N1TbANUT0x3QVwDk0RBvdR-3_2jr/view?usp=sharing

df['slopeMA40'] = df['MA40'].rolling(window=backrollingN).apply(get_slope)...
df['slopeMA80'] = df['MA80'].rolling(window=backrollingN).apply(get_slope)...
df['slopeMA160'] = df['MA160'].rolling(window=backrollingN).apply(get_slope)...
df['slopeAverage'] = df['Average'].rolling(window=backrollingN).apply(get_slope)...
df['slopeRSI'] = df['RSI'].rolling(window=backrollingN).apply(get_slope)...

print(df) # negative slope = down trend. positive slope = uptrend

# The Analysis
'''
take a bar, set an upper limit (take profit) and a lower limit (stop loss). 
Category 0 - if the trend oscillates between the TP and SL then the trend is unclear
Category 1 - if the trend is moving towards the stop loss, then we are in a down trend
Category 2 - if the trend is moving towards the take profit, then it is an up trend
'''

# Target flexible way
pipdiff = 450*1e-5 # for TP. This is a variable
SLTPRatio = 2 #pipdiff/Ratio gives SL

def mytarget(barsupfront, df1):
    length = len(df1)
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])
    trendcat = [None] * length

    for line in range(o, length-barsupfront-2):
        valueOpenLow = 0
        valueOpenHigh = 0
        for i in range(1, barsupfront+2):
            value1 = open[line+1] - low[line+i]
            value2 = open[line+1] - high[line+i]
            valueOpenLow = max(value1, valueOpenLow)
            valueOpenHigh = min(value2, valueOpenHigh)
            ## GET THE Complete code as it does not show in the video
            # https://drive.google.com/file/d/1JTm6N1TbANUT0x3QVwDk0RBvdR-3_2jr/view?usp=sharing

    return trendcat

# my target(bars to take into account, dataframe)
df['mytarget'] = mytarget(16, df)
print(df)

# the tutorial goes along ploting histograms of calculated values
