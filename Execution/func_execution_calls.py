from config_execution import session_private
from config_execution import limit_order_basis
from func_calculation import get_trade_details
from pybit import usdt_perpetual
from config_execution import ticker_1
import math
from time import sleep



# Set leverage
def set_leverage(ticker):

    # Setting the leverage
    try:
        leverage_set = session_private.cross_isolated_margin_switch(
            symbol=ticker,
            is_isolated=True,
            buy_leverage=1,
            sell_leverage=1
        )
        print(leverage_set)
    except Exception as e:
        print(e)
        pass 

    return 

# Place limit or market order

def place_order(ticker, price, quantity, direction, stop_loss):

    # set variable
    if direction == "Long":
        side = "Buy"
    else:
        side ="Sell"
    

    # Place limiet order
    if limit_order_basis:
        order = session_private.place_active_order(
            symbol=ticker,
            side=side,
            order_type="Limit",
            qty=quantity,
            price = price,
            time_in_force="PostOnly",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss = stop_loss
        ) 
    else:
        order = session_private.place_active_order(
            symbol=ticker,
            side=side,
            order_type="Market",
            qty=quantity,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss = stop_loss
        )

    return order



########################################################################

counts = 0

def initialise_order_execution(orderbook, direction, capitial):
    mid_price, stop_loss, quantity = get_trade_details(orderbook, direction, capitial)
   
    global counts
    if quantity > 0 and counts == 0:
        order = place_order(ticker_1, mid_price, quantity, direction, stop_loss)
        # counts += 1
        if "result" in order.keys():
            if "order_id" in order["result"]:
                return order["result"]["order_id"]
    
    return 0


# def handle_message(msg):
#     orderbook = msg["data"]
#     if orderbook:
#         initialise_order_execution(orderbook, "Short", 1000)

# ws_linear.orderbook_25_stream(
#     handle_message, ticker_1
# )

# while True:
#     sleep(1)
#     break



   

    


#########################################################################




    
    
    





