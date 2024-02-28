import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

ticker = ["MSFT"]
df = yf.download(ticker,start="2000-01-01",end="2023-12-31")
df.head()

df_closed = df.loc[:,"Close"].to_frame()
roczny = df_closed.resample(rule="A", kind = "period").last()
lata = year.index.size
roczny["zwrot"] = np.log(roczny.Close/roczny.Close.shift(periods=1))
windows = [year for year in range(years,0,-1)]

for rok in windows:
    roczny[f"{rok}Y"] = roczny.zwrot.rolling(rok).mean()
roczny.tail(15)
triangle = roczny.drop(columns=["Close","zwrot"])

plt.figure(figsize=(30,20))
sns.set(font_scale=1.3)
sns.heatmap(triangle,annot=True,fmt=".1%",cmap="RdYlGn",vmin=-0.4,vmax=0.15,center=0)
plt.tick_params(axis="y",labelright=True)


#for 100 PLN (or other for fixed FX):

ticker = ["MSFT"]
df = yf.download(ticker,start="2000-01-01",end="2023-12-31")
df_closed = df.loc[:,"Close"].to_frame()
roczny = df_closed.resample(rule="A", kind = "period").last()
lata = year.index.size
roczny["zwrot"] = np.log(roczny.Close/roczny.Close.shift(periods=1))
roczny.dropna(inplace=True)
windows = [year for year in range(years,0,-1)]

for rok in windows:
    roczny[f"{rok}Y"] = np.exp(rok*roczny.zwrot.rolling(rok).mean()) * 100

traingle = roczny.drop(columns=["Close","zwrot"])
plt.figure(figsize=(30,20))
sns.set(font_scale=1.3)
sns.heatmap(traingle, annot=True, fmt=".0f", cmap="RdYlGn",vmin=70,vmax=200, center=100)
plt.tick_params(axis="y",labelright=True)



