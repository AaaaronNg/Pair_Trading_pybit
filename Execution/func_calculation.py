from config_execution import stop_loss_fail_safe
from config_execution import ticker_1
from config_execution import ticker_2
from config_execution import rounding_ticker_1
from config_execution import rounding_ticker_2
from config_execution import quantity_rounding_ticker_1
from config_execution import quantity_rounding_ticker_2
import math
from time import sleep


# Puts all close prices in a list
def extract_close_prices(prices):
    close_prices = []
    for price_values in prices:
        if math.isnan(price_values["close"]):
            return []
        close_prices.append(price_values["close"])
    return close_prices

# get trade details and latest prices
def get_trade_details(orderbook, direction="Long", capital=0):

    # set calculation and output variables
    price_rounding = 20
    quantity_rounding = 20
    mid_price = 0
    quantity = 0
    stop_loss = 0
    bid_items_list = []
    ask_item_list = []

    # Get
    if orderbook:

        # Set price rounding
        price_rounding = rounding_ticker_1 if orderbook[0]["symbol"] == ticker_1 else rounding_ticker_2
        quantity_rounding = quantity_rounding_ticker_1 if orderbook[0]["symbol"] == ticker_1 else quantity_rounding_ticker_2

        # Organise prices
        for level in orderbook:
            if level["side"] == "Buy":
                bid_items_list.append(float(level["price"]))
            else:
                ask_item_list.append(float(level["price"]))

        # Calculate price, size, stop loss and average liquidity
        if len(ask_item_list) > 0 and len(bid_items_list)>0:
            bid_items_list.sort()
            ask_item_list.sort()
            bid_items_list.reverse()


            # Get nearest ask, nearest bid and orderbook spread
            nearest_ask = ask_item_list[0]
            nearest_bid = ask_item_list[0]

            

            # Calculate hard stop loss
            if direction == "Long":
                mid_price = nearest_bid
                stop_loss = round(mid_price * (1-stop_loss_fail_safe), price_rounding)
            else:
                mid_price = nearest_ask
                stop_loss = round(mid_price*(1+stop_loss_fail_safe), price_rounding)

            # calculate quantity
            quantity = round(capital/mid_price, quantity_rounding)

    # Output results
    return (mid_price, stop_loss, quantity)




# For checking the latest data 

# from time import sleep
# from pybit import usdt_perpetual
# ws_inverseP = usdt_perpetual.WebSocket(
#     test=True,
#     ping_interval=30,  # the default is 30
#     ping_timeout=10,  # the default is 10
#     domain="bybit"  # the default is "bybit"
# )
# def handle_message(msg):
#     mid_price_1,_, _, = get_trade_details(msg["data"])
#     print(mid_price_1)
# # To subscribe to multiple symbols,
# # pass a list: ["BTCUSD", "ETHUSD"]
# ws_inverseP.orderbook_25_stream(
#     handle_message, ticker_1
# )
# while True:
#     sleep(1)