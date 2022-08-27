from config_execution import signal_negative_ticker
from config_execution import signal_positive_ticker
from config_execution import session_private

# Get position information when you have long or short position
def get_position_info(ticker):
    side = 0
    size = ""
    position = session_private.my_position(
        symbol=ticker
    )
    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            if len(position["result"]) == 2:
                if position["result"][0]["size"] > 0:
                    size = position["result"][0]["size"]
                    side = "Buy"
                else:
                    size = position["result"][1]["size"]
                    side = "Sell"

    return side, size


# Place market close order
def place_market_close_order(ticker, side, size):
    # close position
    session_private.place_active_order(
        symbol=ticker,
        side=side,
        order_type="Market",
        qty=size,
        time_in_force="GoodTillCancel",
        reduce_only=True,
        close_on_trigger=False
    )

    return 

# Close all positions for both tickers
def close_all_positions(kill_switch):

    # Cancel all active orders
    session_private.cancel_all_active_orders(
        symbol=signal_positive_ticker
    )
    session_private.cancel_all_active_orders(
        symbol=signal_negative_ticker
    )

    # Get position information 
    side_1, size_1 = get_position_info(signal_positive_ticker)
    side_2, size_2 = get_position_info(signal_negative_ticker)

    if size_1 > 0:
        place_market_close_order(signal_positive_ticker, side_2,size_1)
    if size_2 > 0:
        place_market_close_order(signal_negative_ticker, side_1, size_2)

    kill_switch = 0
    return kill_switch


