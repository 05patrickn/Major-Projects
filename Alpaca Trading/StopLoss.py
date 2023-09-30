from alpaca.trading.enums import OrderType
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

API_KEY = "PKBL1QALIATJ883NK37N"
SECRET_KEY = "5nFTdbXqa5mVKUzOShjtyCfpFc8HwXRM5BxqVdlA"

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)


# Update the stop_order_data dictionary to include 'symbol' directly
stop_order_data = {
    "qty": 0.1,
    "side": OrderSide.SELL,
    "type": OrderType.STOP,
    "time_in_force": TimeInForce.GTC,
    "symbol": "ETH/USD",  # Include the symbol here
    "stop_price": 2000.0  # Adjust this to your desired stop price
}

# Place the stop-loss order
stop_order = trading_client.submit_order(**stop_order_data)

# Print the response
for property_name, value in stop_order.items():
    print(f"\"{property_name}\": {value}")



# Print the response
for property_name, value in stop_order.items():
    print(f"\"{property_name}\": {value}")
