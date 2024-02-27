import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

ticker = ["MSFT","AAPL","IBM","AMD","KO"]
df_ticker = yf.download(ticker, start = "2013-01-01",end = "2023-12-04")
df_closed = df_ticker.loc[:,"Close"]

daily_return = df_closed.pct_change().dropna()
daily_return.head()

plt.figure(figsize=(10,6))
sns.heatmap(daily_return.corr(), cmap="Reds",annot=True,vmax=0.8)
