ticker = ["MSFT"]
df = yf.download(ticker,start = "1986-01-01",end="2023-12-04")
df_closed = df.loc[:,"Close"].to_frame()
mont_ret = df_closed.resample(rule="M", kind="period").last().pct_change().dropna()

for year in [1,3,5,10]:
    mont_ret[f"{year}Y"] = mont_ret.Close.rolling(year*12).mean() * 12

ax = mont_ret.iloc[:,-4:].plot(figsize=(10,6),subplots=False,sharey=False)
ax.axhline(y=0,color='black',linewidth=1)

axes = mont_ret.iloc[:,-4:].plot(figsize=(10,6),subplots=True,sharey=False)
for ax in axes:
    ax.axhline(y=0,color='black',linewidth=1)
    
