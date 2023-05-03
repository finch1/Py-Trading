# https://www.youtube.com/watch?v=LrWrhNLmu18
# https://www.youtube.com/watch?v=fWHQwqT3lNY - Algovibes Explains in Excel
'''
Daily Return (Daily Percentage Change)

This informs you of the percentage gain or loss. 
Return = (Price Now - Price Before) / Price Before
or
Return at time T = (Price Now / Price Before) -1

A higher number = more volatility
'''

import numpy as np
import pandas as pd

data = pd.read_csv("")

data['Daily_return'] = (data['Adj Close'] / data['Adj Close'].shift(1)) -1
data['Daily_return_pct'] = data['Close'].pct_change(1) # 1  = one day period

'''
Log return Are time additive
'''
# trigger warning on big changes
data['Daily_return_log'] = np.log(data['Close']/data['Close'].shift(1))

'''
Cumulative Daily Return

Is the entire amount of money an investment has earned for an investor, 
irrespective of time. Annualized return is the amount of money the investment
has earned for the investor in one year. This is different than just the stock 
price at the current day, because it will take into account the daily returns.
'''
# are you sure we can sum dailyreturn not the dailyreturn log?
data['Cumulative_return'] = np.cumsum(data['Daily_return'])

'''
Cumulative Return (Compound Factor)

The compund return is the rate of return, usually expressed as a percentage, that represents the cumulative
effect that a series of gains or losses has on an original amount of capital over a period of time.

If I invested $1 in the company, at the beginning of the time series, how much would this be worth today?

Ii = (1 + Rt) * It-1
Multiplying our previous investment of I at t-1 by 1+percent returns. 
'''

data['Cumulative_return_comp'] = (1 + data['Daily_return']).cumprod()

