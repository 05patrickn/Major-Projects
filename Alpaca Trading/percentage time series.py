import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Ticker symbols for S&P 500 and NVDA
tickers = ["^GSPC","AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "FB", "TSLA", "BRK.B", "JNJ"]


# Get daily data for the past year for the tickers
historical_data = yf.download(tickers, period="1y", interval="1d")["Close"]

# Transform data into a pandas DataFrame
df = pd.DataFrame(historical_data)

# Calculate percentage change for each ticker and store in a new DataFrame
percent_change_df = pd.DataFrame()
for ticker in tickers:
    percent_change_df[ticker] = ((historical_data[ticker] - historical_data[ticker].iloc[0]) / historical_data[ticker].iloc[0]) * 100

# Plot the percentage change for each ticker
percent_change_df.plot(figsize=(10, 6))
plt.title("Cumulative Percentage Change of Stocks over a Year")
plt.xlabel("Date")
plt.ylabel("Percentage Change")
plt.show()
