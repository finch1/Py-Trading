# https://www.youtube.com/watch?v=33qz3LIdwKo&list=PLwEOixRFAUxZmM26EYI1uYtJG39HDW1zm&index=7
import pandas as pd

df = pd.read_csv("")
print(df)

## IDENTifying the Engulfing candle patterns
# Engulfing pattern signals
# import random
def Revsignal1(df1):
    length = len(df1)
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])
    signal = [0] * length # 0 = no engulfing candles. 2 = bullish englfing signal. 1 = bearish engulfing signal.
    bodydiff = [0] * length # absolute diff between open and close of a stick. 

    for row in range(1, length):
        bodydiff[row] = abs(open[row] - close[row])
        bodydiffmin = 0.003 # ignore candles sticks where the market is not sure. 
        
        ## COPY THE CODE as it is not completley visible
        # https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbFRzSUpYdkhDbjhVdXRjQ1REM3k0bGphbllfUXxBQ3Jtc0trYnlXU2t2YTVfSkhid1FSRm5xZWo4cjVyQ2ZtZGxTem02RVZnSVZkOHBlSDJpNVA4d1FFLVJfQnFBMjR0RFh5Z1c0MkpwdUNvVUk0eS0tRXoxRWYxUjlmRUZESWFjUE95X29EM242bzRBbmthQk5ZRQ&q=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F112PGLxL4TpoR_DeyCzMi0SgegipSyHWq%2Fview%3Fusp%3Dsharing

        return signal


df['signal1'] = Revsignal1(df)
# to make sure everythign is working properly
df[df['signal1'] == 1].count()