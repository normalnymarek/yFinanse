import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.float_format','{:2f}'.format)

ticker = ["MSFT"]
df = yf.download(ticker, start = "2023-01-01", end = "2023-12-04")
df_closed = df.loc[:,"Close"].to_frame()
df_closed.head()

df_closed.pct_change().dropna()

dzienny_zwrot = pd.DataFrame()
dzienny_zwrot["dzienny_zwrot"] = df_closed.pct_change().dropna()
dzienny_zwrot.info()

plt.style.use("ggplot")
dzienny_zwrot.plot(kind="hist", bins = 100, figsize=(10,6))

avg_daily_return = dzienny_zwrot.mean()
std_dev_daily_return = dzienny_zwrot.std()

MULTIPLIER = 252

ann_avg_return = avg_daily_return * MULTIPLIER
ann_std_dev_daily_return = std_dev_daily_return * np.sqrt(MULTIPLIER)

ticker = ["MSFT","AAPL","IBM","AMD"]
df_ticker = yf.download(ticker, start = "2023-01-01", end = "2023-12-04")
df_closed = df_ticker.loc[:,"Close"]
df_closed.head()

daily_return = df_closed.pct_change().dropna()
daily_return.describe().T

statistics = daily_return.describe().T.loc[:,["mean","std"]]
statistics["mean"] = statistics["mean"] * MULTIPLIER
statistics["std"] = statistics["std"] * np.sqrt(MULTIPLIER)

statistics.plot.scatter(x="std",y="mean",figsize=(10,6), s=40)
for i in statistics.index:
    plt.annotate(i,xy=(statistics.loc[i,"std"]+0.003,statistics.loc[i,"mean"]+0.004),size=14)
plt.title("Roczny zwrot i odchylenie standardowe")
