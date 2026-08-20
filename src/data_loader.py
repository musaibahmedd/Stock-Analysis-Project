import yfinance as yf
import matplotlib.pyplot as plt

stock = yf.Ticker("AAPL")
data = stock.history(period="1y")
data = data.dropna(subset=["Close"])

data["Daily_Return"] = data["Close"].pct_change()
data["Daily_Return_Percent"] = data["Daily_Return"] * 100

data["MA_5"] = data["Close"].rolling(window=5).mean()#.rolling(window=5)Take the prices in groups of 5 days, moving forward one day at a time.
data["MA_20"] = data["Close"].rolling(window=20).mean()

data["Signal"] = (data["MA_5"] > data["MA_20"]).astype(int)
data["Signal_Change"] = data["Signal"].diff()   ##.diff =Current value − previous value

data["Trade_Signal"] = data["Signal_Change"]
data["Position"] = data["Signal"].shift(1).fillna(0) ##.shift(1) because we don't want the algorithm to magically know today's closing price and then pretend it traded earlier that same day.


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

print("Signal Changes:")
print(data[["Signal", "Signal_Change"]].tail(10))   ##tail(10)?We want to see the last 10 trading days and compare.

print("Crossover Events:")
print(data[data["Signal_Change"] != 0][["Close", "MA_5", "MA_20", "Signal_Change"]])
                               #data["Signal_Change"] != 0----Show me only the rows where the signal changed.

print("Trade Signals:")
print(data[data["Trade_Signal"] != 0][["Close", "MA_5", "MA_20", "Trade_Signal"]])
#We're deliberately filtering out all the 0s because hundreds of HOLD days aren't useful to look at.

print("Positions:")
print(data[["Close", "Signal", "Trade_Signal", "Position"]].tail(15))


data["Strategy_Return"] = data["Position"] * data["Daily_Return"] #Strategy_Return = what our strategy earned that day.
data["Cumulative_Strategy_Return"] = (1 + data["Strategy_Return"]).cumprod() #Cumulative_Strategy_Return = how ₹1 would have grown using our strategy.
data["Cumulative_Buy_Hold"] = (1 + data["Daily_Return"]).cumprod() #how ₹1 would have grown if we simply bought AAPL and held it.
data["Strategy_Peak"] = data["Cumulative_Strategy_Return"].cummax()
data["Drawdown"] = (data["Cumulative_Strategy_Return"] / data["Strategy_Peak"]) - 1


strategy_return = (data["Cumulative_Strategy_Return"].iloc[-1] - 1) * 100
buy_hold_return = (data["Cumulative_Buy_Hold"].iloc[-1] - 1) * 100
print("Strategy Return:", f"{strategy_return:.2f}%")
print("Buy & Hold Return:", f"{buy_hold_return:.2f}%")


max_drawdown = data["Drawdown"].min() * 100
print("Maximum Drawdown:", f"{max_drawdown:.2f}%")

average_strategy_return = data["Strategy_Return"].mean()
strategy_volatility = data["Strategy_Return"].std()
sharpe_ratio = (average_strategy_return / strategy_volatility) * (252 ** 0.5)  # √252 We're using approximately 252 trading days in a year to convert our daily Sharpe calculation into an annualized one.
print("Sharpe Ratio:", f"{sharpe_ratio:.2f}")



plt.figure(figsize=(12, 6))

plt.plot(data.index, data["Close"], label="AAPL Close")
plt.plot(data.index, data["MA_5"], label="MA-5")
plt.plot(data.index, data["MA_20"], label="MA-20")

buy_signals = data[data["Trade_Signal"] == 1]  #only finds and stores the BUY rows.
plt.scatter(buy_signals.index, buy_signals["Close"], label="BUY")

sell_signals = data[data["Trade_Signal"] == -1]
plt.scatter(sell_signals.index, sell_signals["Close"], label="SELL")

plt.xlabel("Date")
plt.ylabel("Price ($)")

plt.title("AAPL Stock Price")

plt.legend()





plt.figure(figsize=(12, 6))

plt.plot(
    data.index,
    data["Cumulative_Strategy_Return"],
    label="Strategy"
)

plt.plot(
    data.index,
    data["Cumulative_Buy_Hold"],
    label="Buy & Hold"
)

plt.xlabel("Date")
plt.ylabel("Growth of ₹1")
plt.title("Strategy vs Buy & Hold")
plt.legend()
plt.show()


plt.figure(figsize=(12, 6))
plt.plot(
    data.index,
    data["Drawdown"],
    label="Strategy Drawdown"
)

plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.title("Strategy Drawdown")
plt.legend()
plt.show()