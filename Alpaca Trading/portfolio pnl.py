import alpaca_trade_api as tradeapi
from datetime import datetime

# Initialize Alpaca API
API_KEY = ""
SECRET_KEY = ""
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

# Get open positions
positions = api.list_positions()

# Define the portfolio start date (replace with your actual start date)
portfolio_start_date = datetime(2023, 9, 21) #FIXME

# Print the positions and calculate total unrealized PnL
total_unrealized_pnl = 0
for position in positions:
    print("Symbol:", position.symbol)
    print("Quantity:", position.qty)
    print("Side:", position.side)
    print("Current Price:", position.current_price)
    print("Market Value:", position.market_value)
    print("Unrealized PnL:", position.unrealized_pl)
    print("============================")

    total_unrealized_pnl += float(position.unrealized_pl)

print(" \n ")

# Calculate percentage PnL since the portfolio start date
initial_investment = 100000  # Adjust this with your actual initial investment

# Calculate the current portfolio value (investment + total unrealized PnL)
current_portfolio_value = initial_investment + total_unrealized_pnl

# Calculate the percentage PnL
percentage_pnl = ((current_portfolio_value - initial_investment) / initial_investment) * 100

print("Total Unrealized PnL: {:.2f}".format(total_unrealized_pnl))
print(f"Percentage PnL since portfolio start date {portfolio_start_date.strftime('%Y-%m-%d')}: {percentage_pnl:.2f}%")
