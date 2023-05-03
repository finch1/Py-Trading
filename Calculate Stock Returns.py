# https://www.youtube.com/watch?v=fWHQwqT3lNY

'''
return = (current - prev ) / prev
return = (current / prev) - (prev / prev) == (current / prev) - 1

one day return calc. (the results cannot be summed as a total return for x number of days as the answer will be incorrect)
return = (today / yesterday) - 1

5 day return calc
return = (day 5 / day1) - 1

cumulative return = (1 + today's return) * (1 + yesterday's cumret) - 1
cumulative return should equal x day return if both are done for the same x number of days

log return. willl provide a result close to 'return calc' and the results can be summed
log return = LN(1 + one day return)

then for x number of day = EXP(SUM(log returns)-1)
using log returns will show a better scaling of profits, day to day
'''

import yfinance as yf
import numpy as np

df = yf.download('TSLA', start='2021-12-21')

changes = df['Adj Close'].pct_change()
print(changes)

# 4 day cumulative return
returns = (df['Adj Close'] / df['Adj Close'].shift(3)) - 1
print(returns)

cumulatedret = (1 + changes).cumprod() -1
print(cumulatedret)

logret = np.exp(np.log(1 + changes).cumsum()) - 1
print(logret)