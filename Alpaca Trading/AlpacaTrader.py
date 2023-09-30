from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


API_KEY = "PKBL1QALIATJ883NK37N"
SECRET_KEY = "5nFTdbXqa5mVKUzOShjtyCfpFc8HwXRM5BxqVdlA"

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

"""
account = trading_client.get_account()
for property_name, value in account:
  print(f"\"{property_name}\": {value}")
  
  
"""  

# Setting parameters for our buy order
market_order_data = MarketOrderRequest(
                      symbol="GOOGL",
                      qty=1,
                      side=OrderSide.SELL,
                      time_in_force=TimeInForce.GTC
                  )

# Market Order
confirm_order=input("Confirm order: Y/N \n")
if confirm_order=="Y":
    market_order = trading_client.submit_order(market_order_data)
    for property_name, value in market_order:
      print(f"\"{property_name}\": {value}")
    else:
        print("Order rejected")
        
