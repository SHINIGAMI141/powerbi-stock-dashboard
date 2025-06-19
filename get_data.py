"""
get_data.py

This script downloads historical stock index data using yfinance,
calculates 8-day and 21-day EMAs (Exponential Moving Averages),
generates simple trading signals based on EMA crossovers,
and outputs a cleaned dataset for use in a Power BI dashboard.

Tickers included:
- S&P 500 (^GSPC)
- Dow Jones Industrial (^DJI)
- Nasdaq Composite (^IXIC)
- Russell 2000 (^RUT)

Dependencies:
- yfinance
- pandas
- pandas_ta

Usage:
Run this script to produce 'dataset.csv', which serves as the data source
for the Power BI dashboard visualizing price, volume, EMAs, and signals.
Alternatively, comment out the line 'dataset.to_csv("dataset.csv", index=False)'
to use the script directly within Power BI's Python data connector.
"""
import yfinance as yf
import pandas as pd
import pandas_ta as ta


def EMA_CROSS(candleData, fast=8, slow=21):
    df = candleData
    fast_ema = f"EMA_{fast}"
    slow_ema = f"EMA_{slow}"

    df[fast_ema] = ta.ema(close=df["Close"], length=fast, append=True)
    df[slow_ema] = ta.ema(close=df["Close"], length=slow, append=True)

    previous_fast = df[fast_ema].shift(1)
    previous_slow = df[slow_ema].shift(1)
    sell_crossing = (df[fast_ema] <= df[slow_ema]) & (previous_fast >= previous_slow)
    buy_crossing = (df[fast_ema] >= df[slow_ema]) & (previous_fast <= previous_slow)

    df["buy"] = buy_crossing
    df["sell"] = sell_crossing

    df["Action"] = "NA"
    df.loc[df["buy"] == True, "Action"] = "LONG ALERT"
    df.loc[df["sell"] == True, "Action"] = "SHORT ALERT"

    df.loc[df["Action"] == "LONG ALERT", "Signal"] = "Enter Long at " + (1.01 * df.loc[df["Action"] == "LONG ALERT", "High"]).round(2).astype(str)
    df.loc[df["Action"] == "SHORT ALERT", "Signal"] = "Enter Short at " + (0.99 * df.loc[df["Action"] == "SHORT ALERT", "Low"]).round(2).astype(str)

    returnColumns = ["Date","Open", "High", "Low", "Close", "Volume", fast_ema, slow_ema, "Signal"]
    returndf = df[returnColumns]
    return returndf


tickers = ["^GSPC", "^DJI", "^IXIC", "^RUT"]
ticker_names = ["S&P 500", "Dow Jones Industrial", "Nasdaq Composite", "Russell 2000"]

all_data = []

for ticker, ticker_name in zip(tickers, ticker_names):
    data = yf.download(ticker, start="2020-01-01", progress=False)
    data.reset_index(inplace=True)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    df = EMA_CROSS(data, fast=8, slow=21)

    df["Ticker"] = ticker_name

    all_data.append(df)

dataset = pd.concat(all_data, ignore_index=True)

dataset.to_csv("dataset.csv", index=False)
