# https://www.youtube.com/watch?v=Km2KDo6tFpQ

import streamlit as st
import yfinance as yf
import pandas as pd


def relativeret(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

st.title('LIT Finance Dashboard')
tickers = ("BTC-EUR", "LINK-EUR", "VET-EUR", "ADA-EUR", "MATIC-EUR")

# define input
dropdown = st.multiselect('P!ck your assts', tickers)
start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))

# choosing a ticker. the program checks if the field is populated
if len(dropdown) > 0:
    df = relativeret(yf.download(dropdown, start=start, end=end)['Adj Close'])
    st.header('Returns of {}'.format(dropdown))
    st.line_chart(df)