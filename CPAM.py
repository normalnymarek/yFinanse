import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style("whitegrid")

pd.set_option('display.float_format', '{:.4f}'.format)

ticker = ["MSFT", "AAPL", "IBM", "KO", "BA", "AMZN"]
df = yf.download(ticker, start="2010-01-01", end="2023-12-31")
df.head()

portfolio = df["Adj Close"]
ret = portfolio.pct_change().dropna()
ret.head()

def ann_risk_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate the annualized risk return.

    :param df: Pandas DataFrame containing the risk and return data.
    :type df: pd.DataFrame
    :return: A DataFrame with the annualized risk and return.
    :rtype: pd.DataFrame
    """
    summary = df.agg(func=["mean", "std"]).T
    summary.columns = ["zwrot", "ryzyko"]
    summary.zwrot = summary.zwrot * 252  # calculate the annualized return
    summary.ryzyko = summary.ryzyko * np.sqrt(252)  # calculate the annualized risk
    return summary

summary = ann_risk_return(ret)
summary["wariancja"] = np.power(summary.ryzyko, 2)
RISK_FREE_RATE = 0.03
summary["sharpe"] = summary.zwrot.sub(RISK_FREE_RATE).div(summary.ryzyko)
liczba_akcji = len(summary.index)
liczba_portfeli = 150000

np.random.seed(seed=123)
matrix = np.random.random(liczba_akcji * liczba_portfeli).reshape(liczba_portfeli, liczba_akcji)
wagi = matrix / matrix.sum(axis=1, keepdims=True)
port_ret = ret.dot(wagi.T)

port_summ = ann_risk_return(port_ret)
port_summ["sharpe"] = port_summ.zwrot.sub(RISK_FREE_RATE).div(port_summ.ryzyko)

max_sharpe_id = port_summ.sharpe.idxmax()

max_sharp_stat = port_summ.iloc[max_sharpe_id]

max_sharp_wagi = wagi[max_sharpe_id, :]

best_wagi = pd.Series(index=ret.columns, data=max_sharp_wagi)

ret["Portfel"] = port_ret[max_sharpe_id]

summary = pd.concat([summary, pd.DataFrame({"zwrot": 0.268141, "ryzyko": 0.242881, "sharpe": 0.980484}, index=["Portfel"])])
summary["wariancja"] = np.power(summary.ryzyko, 2)
summary
cov = ret.cov() * 252
summary.ryzyko_systematyczne / summary.loc["Portfel", "ryzyko_systematyczne"]
summary["beta"] = summary.ryzyko_systematyczne / summary.loc["Portfel", "ryzyko_systematyczne"]
plt.style.use("ggplot")
plt.figure(figsize=(10,6))
plt.scatter(summary.beta, summary.zwrot)
for i in summary.index:
    plt.annotate(i, xy=(summary.loc[i, "beta"]+0.004, summary.loc[i, "zwrot"]+0.004))
plt.plot([0, summary.loc["AAPL", "beta"]-0.015], [RISK_FREE_RATE, summary.loc["AAPL", "zwrot"]])
plt.scatter(0, RISK_FREE_RATE, s=100, marker="x", c="blue")
plt.xlabel("beta")
plt.ylabel("annual return")
plt.title("beta / zysk")

RISK_FREE_RATE + (summary.loc["Portfel", "zwrot"] - RISK_FREE_RATE) * summary.loc["AAPL", "beta"]
summary["capm_zwrot"] = RISK_FREE_RATE + (summary.loc["Portfel", "zwrot"] - RISK_FREE_RATE) * summary.beta
summary["wagi"] = best_wagi
summary["alpha"] = summary.zwrot - summary.capm_zwrot





