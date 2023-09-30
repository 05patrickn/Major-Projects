import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

period="6mo"
# Ticker symbols for S&P 500 and NVDA
tickers = ["^GSPC", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "JNJ"]

# Get daily data for the past year for the tickers
historical_data = yf.download(tickers, period=period, interval="1d")["Close"]

# Calculate percentage change for each ticker and store in a new DataFrame
percent_change_df = pd.DataFrame()
for ticker in tickers:
    percent_change_df[ticker] = ((historical_data[ticker] - historical_data[ticker].iloc[0]) / historical_data[ticker].iloc[0]) * 100

# Calculate the absolute percentage deviation from S&P 500 for each ticker
abs_deviation_df = percent_change_df.subtract(percent_change_df['^GSPC'], axis=0)
abs_deviation_df.drop('^GSPC', axis=1, inplace=True)
# Plot the absolute percentage deviation for each ticker
abs_deviation_df.plot(figsize=(10, 6))
plt.title(f"Percentage Deviation of Stocks from S&P 500 over {period} period")
plt.xlabel("Date")
plt.ylabel("Absolute Percentage Deviation")
plt.show()
