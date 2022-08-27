from func_position_calls import query_existing_order
from func_position_calls import get_open_position
from func_position_calls import get_active_position
from func_calculation import get_trade_details
from config_execution import session


# check order item
def check_order(ticker, order_id, remaining_capital, direction="Long"):

    # Get current orderbook
    orderbook = session.orderbook(symbol=ticker)

    # get latest price
    mid_price, _, _ = get_trade_details(orderbook["result"])

    # Get trade details
    order_price, order_quantity, order_status = query_existing_order(ticker, order_id, direction)

    # Get open position
    position_price, position_quantity = get_open_position(ticker, direction)

    # Get active positions
    active_order_price, active_order_quantity = get_active_position(ticker)

    # Determin action - position filled - buy more
    if order_status == "Filled":
        return "Position Filled"

    # Determine action - trade complete - stop placing orders
    if position_quantity >= remaining_capital:
        return "Trade Complete"

    # Determine action - order active - do nothing
    active_items = ["Created", "New"]
    if order_status in active_items:
        return "Order Active"
    
    # Determine action - partial filled order - do nothing
    if order_status == "PartiallyFilled":
        return "Partial Filled"

    # Determine action - order failed - try place order again
    cancel_itmes = ["Cancelled", "Rejected", "PendingCancel"]
    if order_status in cancel_itmes:
        return "Try Again"