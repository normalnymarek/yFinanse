import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

ticker = ["MSFT"]
df = yf.download(ticker, start = "2018-01-01",end="2023-12-04")
df_closed=df.loc[:,"Close"].to_frame()

df_closed.describe()
df_closed["sma_50"] = df_closed.rolling(window=50,min_periods=50).mean()
df_closed["sma_200"] = df_closed.Close.rolling(window=200,min_periods=200).mean()

plt.style.use("ggplot")
df_closed.plot(figsize=(10,6))
