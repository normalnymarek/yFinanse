import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

ticker = ["MSFT"]
df = yf.download(ticker,start = "1986-01-01",end="2023-12-04")
df_closed = df.loc[:,"Close"].to_frame()

mont_ret = df_closed.resample(rule="M",kind="period").last().pct_change().dropna()
mont_ret["return"] = mont_ret.rolling(window=36).mean() * 12
mont_ret["risk"] = mont_ret.Close.rolling(window=36).std() * np.sqrt(12)
mont_ret.dropna(inplace=True)

ax = mont_ret.iloc[:,-2:].plot(figsize=(10,6))
ax.axhline(y=0,color='black',linewidth=1)

mont_ret.iloc[:,-2:].corr()
mont_ret.iloc[:,-2:].plot(kind="scatter",x="risk",y="return",figsize=(10,6))
