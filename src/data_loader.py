import yfinance as yf

stock = yf.Ticker("AAPL")
data = stock.history(period="1mo")  #

data["Daily_Return"] = data["Close"].pct_change()
data["Daily_Return_Percent"] = data["Daily_Return"] * 100
data["MA_5"] = data["Close"].rolling(window=5).mean()    #.rolling(window=5)Take the prices in groups of 5 days, moving forward one day at a time.
data["MA_20"] = data["Close"].rolling(window=20).mean()
data["Signal"] = (data["MA_5"] > data["MA_20"]).astype(int)


print("Highest Close:", data["Close"].max())
print("lowest Close:", data["Close"].min())
print("Average Close:", data["Close"].mean())

print("Daily Returns:")
print(data["Daily_Return_Percent"].tail().map(lambda x: f"{x:.2f}%"))
print("Daily Volatility:", f"{data['Daily_Return'].std() * 100:.2f}%")

print("Moving Averages:")
print(data[["Close", "MA_5", "MA_20"]].tail())

print("Trading Signal:")
print(data[["Close", "MA_5", "MA_20", "Signal"]].tail())