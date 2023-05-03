# https://www.youtube.com/watch?v=dnrJ4zwCADM&list=RDCMUC87aeHqMrlR6ED0w2SVi5nw&index=29
# not sure how good this realy is...
import pandas as pd
import yfinance as yf
import pandas_datareader.data as reader
import datetime as dt
from dateutil.relativedelta import relativedelta

# Get ticker symbols fro the stocks contained in DJI
table = pd.read_html("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average")[0] # multiple tables retrieved
tickers = table.Symbol.tolist()

# Get prices for the DJI components
start = dt.datetime(2018,1,31)
end = dt.datetime(2020, 1, 31)

df = reader.get_data_yahoo(tickers, start, end)['Adj Close']

# Calculate monthly returns by cumulating daily returns
mtl_ret = df.pct_change().resample('M').agg(lambda x:(x+1).prod() -1)
print(mtl_ret)

# Calculate returns over the past 11 months
import numpy as np

# Getting past 11 month cumulated returns
past_11 = (mtl_ret+1).rolling(11).apply(np.prod)-1 # 11 months
print(past_11)

# Set Portfolio formation date
formation = dt.datetime(2019,12,31)
end_measurement = formation - relativedelta(months=1)
print(formation, end_measurement)

# Get past 12 months skippping the most recent one. 
ret_12 = past_11.loc[end_measurement]
print(ret_12) # past 12 month performance

# transform to df to manipulate
ret_12 = ret_12.reset_index()
print(ret_12)

ret_12['quintile'] = pd.qcut(ret_12.iloc[:,1],5, labels=False)
print(ret_12)

winner = ret_12[ret_12.quintile == 4] # long
losers = ret_12[ret_12.quintile == 0] # short

# check our monthly returns
winnerret = mtl_ret.loc[formation + relativedelta(months=1), df.columns.isin(winner.Symbols)]


