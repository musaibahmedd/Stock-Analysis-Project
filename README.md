# Stock Analysis Project

A Python project for analyzing AAPL stock data and testing a simple moving average trading strategy.

# What it does

* Downloads 1 year of AAPL stock data using yfinance
* Calculates daily returns and volatility
* Calculates 5-day and 20-day moving averages
* Generates BUY and SELL signals
* Calculates strategy returns
* Compares the strategy with Buy & Hold
* Calculates maximum drawdown and Sharpe ratio
* Creates charts for stock price, strategy performance, and drawdown

The strategy uses two moving averages:

* MA-5: 5-day moving average

* MA-20: 20-day moving average

* A BUY signal is generated when the 5-day moving average moves above the 20-day moving average.

* A SELL signal is generated when the 5-day moving average moves below the 20-day moving average.

* The previous day's signal is used for the position calculation to avoid look-ahead bias.

# Technologies

* Python
* Pandas
* Matplotlib
* yfinance

# Run

```bash
pip install -r requirements.txt
python src/data_loader.py
```

# Note

This project is an analytical and educational project. The trading strategy is a simple moving average strategy and is not intended to be used directly for real-money trading.
