from config_execution import signal_positive_ticker
from config_execution import signal_negative_ticker
from config_execution import signal_trigger_thresh
from config_execution import tradable_capital_usdt
from config_execution import limit_order_basis
from config_execution import session_private
from func_price_calls import get_ticker_trade_liquidity
from func_get_zscore import get_latest_zscore
from func_execution_calls import initialise_order_execution
from func_order_review import check_order
import time


# Manage new trade assessment and order placing
def manage_new_trades(kill_switch):
    
    # set variable
    order_long_id = ""
    order_short_id = ""
    hot = False

    # Get and save the latest z-score
    zscore, signal_sign_positive = get_latest_zscore()


    print(zscore, signal_sign_positive)
    # switch to hot if meets signal threshold
    if abs(zscore) > signal_trigger_thresh:
        hot = True
        print("-- Trade Status HOT --")
        print("-- Placing and Monitoring Existing Trades --")

    if hot and kill_switch == 0:
        # Get trade history for liquidity
        avg_liquidity_ticker_p, last_price_p = get_ticker_trade_liquidity(signal_positive_ticker)
        avg_liquidity_ticker_n, last_price_n = get_ticker_trade_liquidity(signal_negative_ticker)

        # Determine long ticker vs short ticker
        if signal_sign_positive:
            long_ticker = signal_positive_ticker
            short_ticker = signal_negative_ticker
            avg_liquidity_long = avg_liquidity_ticker_p
            avg_liquidity_short = avg_liquidity_ticker_n
            last_price_long = last_price_p
            last_price_short = last_price_n
        else:
            long_ticker = signal_negative_ticker
            short_ticker = signal_positive_ticker
            avg_liquidity_long = avg_liquidity_ticker_n
            avg_liquidity_short = avg_liquidity_ticker_p
            last_price_long = last_price_n
            last_price_short = last_price_p
        
        # Filled targets
        capital_long = tradable_capital_usdt * 0.5
        capital_short = tradable_capital_usdt - capital_long
        initial_fill_target_long_ustd = avg_liquidity_long * last_price_long
        initial_fill_target_short_ustd = avg_liquidity_short * last_price_short
        initial_capital_injection_ustd = min(initial_fill_target_long_ustd, initial_fill_target_short_ustd)

        # Ensure initial cpaitial does not exceed limits set in configuration
        if limit_order_basis:
            if initial_capital_injection_ustd > capital_long:
                initial_capital_usdt = capital_long
            else:
                initial_capital_usdt = initial_capital_injection_ustd
            
        else:
            initial_capital_usdt = capital_long

        
        # Set remaining capital

        remaining_capital_long = capital_long
        remaining_capital_short = capital_short

        print(remaining_capital_long, remaining_capital_short, initial_capital_usdt)



    return 0

