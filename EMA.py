import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style("whitegrid")

ticker=["MSFT"]
df = yf.download(ticker,start = "2020-01-01",end="2023-12-31")
df.head()

df_closed = df.loc[:,"Close"].to_frame()
df_closed.head()

df_closed["sma"] = df_closed.Close.rolling(window=100).mean()
df_closed["ewma"] = df_closed.Close.ewm(span=100,min_periods=100).mean()
df_closed.tail()

#ewm react faster to price changes
df_closed.iloc[:,-2:].plot(figsize=(10,6))


#corr
ticker = ["MSFT","AAPL"]
df = yf.download(ticker, start = "2010-01-01", end = "2023-12-31")
df.head()

df_closed= df.loc[:, [("Close", "MSFT"), ("Close", "AAPL")]]
df_closed.head()

month_ret = df_closed.resample(rule="M",kind="period").last().pct_change().dropna()
month_ret.head()

month_ret.corr()
month_ret.columns

month_ret[ ('Close', 'MSFT')].rolling(12).corr(month_ret[('Close', 'AAPL')]).plot(figsize=(10,6))






