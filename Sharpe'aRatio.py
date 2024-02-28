import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style("whitegrid")

ticker = ["MSFT","AAPL","IBM","KO","BA","AMZN"]

df=yf.download(ticker,start="2010-01-01",end="2023-12-31")
df.head()
portfolio = df["Adj Close"]
portfolio.tail()
portfolio.plot()

ret = portfolio.pct_change().dropna()
ret.head()
ret.mean(axis=1)
liczba_spolek = len(ret.columns)
wagi = [1/liczba_spolek for i in range(liczba_spolek)]
ret["total"] = ret.dot(other=wagi)
summary = ret.agg(func=["mean","std"]).T
summary.columns = ["zwrot","ryzyko"]
summary.zwrot = summary.zwrot*52
summary.ryzyko = summary.ryzyko * np.sqrt(252)

summary.plot(kind="scatter", x="ryzyko",y="zwrot", figsize=(10,6), s=35)
for i in summary.index:
    plt.annotate(i, xy=(summary.loc[i,"ryzyko"]+0.003, summary.loc[i,"zwrot"]+0.003), size =12)
plt.xlabel("roczne ryzyko",fontsize=14)
plt.ylabel("roczny zwrot", fontsize=14)


"""
Different calculation
"""

def ann_risk_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate the annualized risk return
    :param df: Pandas DataFrame containing the risk and return data
    :type df: pd.DataFrame
    :return: A DataFrame with the annalized risk and return
    :rtype: rd.DataFrame
    """
    summary = df.agg(func=["mean","std"]).T
    summary.columns=["zwrot","ryzyko"]
    summary.zwrot=summary.zwrot*252
    summary.ryzyko=summary.ryzyko*np.sqrt(252)
    return summary


ticker = ["MSFT","AAPL","IBM","KO","BA","AMZN"]
df = yf.download(ticker,start="2010-01-01",end="2023-12-31")
df.head()

portfolio = df["Adj Close"]
ret = portfolio.pct_change().dropna()
ret.head()
summary = ann_risk_return(ret)
liczba_akcji = len(summary.index)
liczba_portfeli = 150000
np.random.seed(seed=123)
matrix=np.random.random(liczba_akcji*liczba_portfeli).reshape(liczba_portfeli,liczba_akcji)
matrix.shape

wagi = matrix / matrix.sum(axis=1,keepdims=True)
wagi.sum(axis=1,keepdims=1)
port_ret  = ret.dot(wagi.T)
port_summ = ann_risk_return(port_ret)

sns.set_theme(context="notebook", style="darkgrid",palette="deep")
plt.figure(figsize=(12,6))
plt.scatter(x=port_summ.loc[:,"ryzyko"],y=port_summ.loc[:,"zwrot"],s=15,color="blue",alpha=0.15)
plt.scatter(x=summary.loc[:,"ryzyko"],y=summary.loc[:,"zwrot"],s=15,color="red",marker="x")
for i in summary.index:
    plt.annotate(i, xy = (summary.loc[i,"ryzyko"]+0.003,summary.loc[i, "zwrot"]+0.003),size=12)
plt.xlabel("roczne ryzyko",fontsize=14)
plt.ylabel("roczny zwrot", fontsize=14)
plt.title("zwrot/ryzyko",fontsize=18)


#sharpe ratio, for the risk_free_rate = 0.03
RISK_FREE_RATE = 0.03
summary["sharpe"] = summary.zwrot.sub(RISK_FREE_RATE).div(summary.ryzyko)
#sharpe for our random portfolios:
port_summ["sharpe"] = port_summ.zwrot.sub(RISK_FREE_RATE).div(port_summ.ryzyko)
port_summ.describe()

sns.set_theme(context="notebook",style="darkgrid",palette="deep")
plt.figure(figsize=(12,6))
plt.scatter(
    x = port_summ.loc[:,"ryzyko"],
    y = port_summ.loc[:,"zwrot"],
    s=15,
    c=port_summ.loc[:,"sharpe"],
    cmap="coolwarm",
    alpha=0.15,
    vmin=0.6,
    vmax=0.98
)

plt.scatter(
    x=summary.loc[:,"ryzyko"],
    y=summary.loc[:,"zwrot"],
    s=25,
    c=summary.loc[:,"sharpe"],
    cmap="coolwarm",
    marker="x"
)
plt.colorbar()
for i in summary.index:
    plt.annotate(i,xy=(summary.loc[i,"ryzyko"]+0.003,summary.loc[i,"zwrot"]+0.003),size=12)
plt.xlabel("roczne ryzyko",fontsize=14)
plt.ylabel("roczny zwrot",fontsize=14)
plt.title("zwrot/ryzyko",fontsize=18)






