# https://www.youtube.com/watch?v=ZUQEd22oNek

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

financials = yf.Ticker('AAPL').info

print(financials)

tickers = ['AAPL', 'MSFT', 'IBM']

info  = []

for i in tickers:
    info.append(yf.Ticker(i).info)

# array of dicts into DF where each key becomes a column
df = pd.DataFrame(info)
df = df.set_index('symbol')

fundamentals = ['dividendYield','marketCap', 'beta', 'forwardPE']

# column filtering
fund_df = df[df.columns[df.columns.isin(fundamentals)]]

plt.bar(fund_df.index, fund_df.dividendYield, color=('k', 'orange', 'cyan'))
plt.show()