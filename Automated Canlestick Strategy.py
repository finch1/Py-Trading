# https://www.youtube.com/watch?v=eN4zh3PEH6c

from os import close
import pandas as pd
import numpy as np
import pandas_ta as ta


df = pd.read_csv("")
df['ATR'] = df.ta.atr(length=10)
df['RSI'] = df.ta.rsi()
df.dropna()

# for down trends - Shooting star
def Revsignal1(df1):
    df.dropna()
    df.reset_index(drop=True, inplace=True)

    length = len(df1)
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])

    # define zero valued list
    signal = [0] * length
    highdiff = [0] * length
    lowdiff = [0] * length
    bodydiff = [0] * length
    ratio1 = [0] * length
    ratio2 = [0] * length

    # analysis
    for row in range(0, length):
        highdiff[row] = high[row] - max(open[row], close[row])
        bodydiff[row] = abs(open[row], close[row])
        # if bodydiff is zero ... 0.002 is a chosen magic number
        if bodydiff[row] < 0.002:
            bodydiff[row] = 0.002
        lowdiff[row] = min(open[row], close[row]) - low[row]
        ratio1[row] = highdiff[row]/bodydiff[row]
        ratio2[row] = lowdiff[row]/bodydiff[row]

# shooting star
#   |
#  _|_
# |___|
#   |

        if (ratio1[row] > 2.5 and \
            lowdiff[row] < 0.3 * highdiff[row] and \
            bodydiff[row] > 0.03 and \
            df.RSI[row] > 50 and \
            df.RSI[row] < 71): 
            signal[row] = 1

# inverted shooting star - 
#  _|_
# |___|
#   |            
#   |

        elif (ratio2[row] > 2.5 and \
            highdiff[row] < 0.23 * lowdiff[row] and \
            bodydiff[row] > 0.03 and \
            df.RSI[row] < 55 and \
            df.RSI[row] > 31): 
            signal[row] = 2

    return signal

df['signal'] = Revsignal1(df)
# count buying signals found 
print(df[df['signal']==1].count())

# Target Shooting Star
def mytarget(barsupfront, df1): # how many bars to look ahead  = barsupfront
    length = len(df1)
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])
    datr = list(df1['ATR']) # average to trange
    trendcat = [None] * length

    for line in range (0, length-barsupfront -1):
        valueOpenLow = 0
        valueOpenHigh = 0

        highdiff = high[line] - max(open[line], close[line])
        bodydiff = abs(open[line] - close[line])

        pipdiff = datr[line]*1.0
        if pipdiff < 1.1:
            pipdiff = 1.1

        # check if stop loss has been triggered

        SLTPRatio = 2.0 # pipdiff*Ratio gives TP ( difines the price to take profit gap )

        for i in range(1, barsupfront +1):
            value1 = close[line] - low[line+i]
            value2 = close[line] - high[line+i]
            valueOpenLow = max(value1, valueOpenLow)
            valueOpenHigh = min(value2, valueOpenHigh)

            if ( (valueOpenLow >= (SLTPRatio*pipdiff) ) and (-valueOpenHigh < pipdiff) ):
                trendcat[line] = 1 #-1 downtrend
                break
            elif ((valueOpenLow < pipdiff) ) and (-valueOpenHigh >= (SLTPRatio*pipdiff)):
                trendcat[line] = 2 # uptrend
                break 
            else:
                trendcat[line] = 0 # no clear trend

    return trendcat

# mytarget
df['Trend'] = mytarget(100, df)
print(df)

# Checking if the signal and trend were correct
conditions = [(df['Trend'] == 1) & (df['signal'] == 1),
              (df['Trend'] == 2) & (df['signal'] == 2)]

values = [1,2]
df['result'] = np.select(conditions, values)

trendId = 1
# count buys against total
print(df[df['result']==trendId].result.count()/df[df['signal1']==trendId].signal1.count())



# check the signals against a candle stick graph. 
# print the index  from the dataframe and plot it 
df[ (df['result']!=trendId) & (df['signal1']==trendId) ] # false positives

#histrs = df[ (df['result']==2) & (df['signal1']==2) ].RSI # false positives
#import matplotlib.pyplot as plt
#plt.hist(histrs,bins=2)  # density=False would make counts
#plt.ylabel('Probability')
#plt.xlabel('RSI');

dfpl = df[400:480]
import plotly.graph_objects as go
from datetime import datetime

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['open'],
                high=dfpl['high'],
                low=dfpl['low'],
                close=dfpl['close'])])

fig.show()