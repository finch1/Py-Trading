# https://www.youtube.com/watch?v=JzdVPnCSSuo
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

df = yf.download('TSLA', start = '2020-11-01')

def MACD(df):
    df['EMA12'] = df['Adj Close'].ewm(span=12).mean()
    df['EMA26'] = df['Adj Close'].ewm(span=12).mean()
    df['MACD'] = df.EMA12 - df.EMA26
    df['signal'] = df.MACD.ewm(span=9).mean()


plt.plot(df.signal, label='signal', color='red')
plt.plot(df.MACD, label='MACD', color='green')
plt.legend()
plt.show()

# check against the day before. Starting loop at row 2 to skip zero values
Buy, Sell = [],[]

for i in range(2, len(df)):
    if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i-1] < df.signal.iloc[i-1]:
        Buy.append(i) # row number where the buy should be fullfilled

    elif df.MACD.iloc[i] < df.signal.iloc[i] and df.MACD.iloc[i-1] > df.signal.iloc[i-1]:
        Sell.append(i) # row number where the sell should be fullfilled


plt.scatter(df.iloc[Buy].index, df.iloc[Buy]['Adj Close'],marker="^", label='Buy', color='green' ) # df.iloc[Buy].index = returns the index as date for the row in particular
plt.scatter(df.iloc[Sell].index, df.iloc[Sell]['Adj Close'],marker="v", label='Sell', color='red' )
plt.plot(['Adj Close'], label='TSLA', color='k')
plt.legend()
plt.show()

# how much profit did we make?
RealBuys = [i+1 for i in Buy]# +1 as we are buying afterwards
RealSells = [i+1 for i in Sell]

Buyprices = df.Open.iloc[RealBuys] # returns the days as the index
Selprices = df.Open.iloc[RealSells]

# in certain cases if there is no buy before the sell of opposite, the profit cannot be calculated
if Selprices.indes[0] < Buyprices.index[0]:
    Selprices = Selprices.drop(Selprices.index[0])
# not sure about the elif or if it should be if
elif Buyprices.index[0] > Selprices.indes[-1]:
    Buyprices = Buyprices.drop(Buyprices.index[-1])

profitsrel = []

for i in range(len(Selprices)):
    profitsrel.append((Selprices[i] - Buyprices[i])/Buyprices[i])

print(profitsrel) # any negatives mean loss so the strategy needs to be fixed

# average profit
print(pd.DataFrame(profitsrel).mean())