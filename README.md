# 📈 Power BI Stock Market Dashboard

This project visualizes stock market data using Power BI and technical indicators generated with Python.

## 🔧 Tools Used

- 🐍 Python (`yfinance`, `pandas`, `pandas_ta`)
- 📊 Power BI Desktop
- 📁 Data: OHLCV for S&P 500, Dow Jones, Nasdaq, and Russell 2000

## 📄 Features

- Volume + Close + EMA(8) + EMA(21) over time (line + stacked column chart)
- Ticker and Date slicers for interactivity
- Signal table with strategy alerts (Enter Long/Short)
- Easy to scale or modify with your own stocks/indicators

## 🧠 Strategy Insight

The dashboard implements a simple EMA crossover system:
- **LONG Alert** when EMA(8) crosses above EMA(21)
- **SHORT Alert** when EMA(8) crosses below EMA(21)

## 📂 Files

- `get_data.py`: Script to download index data, calculate EMAs and signals
- `dataset.csv`: Output from Python, used as data source for Power BI
- `dashboard.pbix`: The Power BI dashboard file
- `screenshots/dashboard-preview.png`: Visual of the dashboard

## 🔄 How to Use

1. Run `get_data.py` to generate `dataset.csv`
2. Open `dashboard.pbix` in Power BI Desktop
3. Refresh data in Power BI to load updated data
4. Use the slicers to filter by ticker and date

---

Feel free to fork or expand this project!
