from config_execution import ticker_1
from config_execution import ticker_2
from func_calculation import get_trade_details
from config_execution import session
from func_price_calls import get_latest_klines
from func_stats import calculate_metrics
from time import sleep


def get_latest_zscore():
    # Get latest asset orderbook prices
    orderbook_1 = session.orderbook(symbol=ticker_1)
    mid_price_1,_, _, = get_trade_details(orderbook_1["result"])
    orderbook_2 = session.orderbook(symbol=ticker_2)
    mid_price_2,_, _, = get_trade_details(orderbook_2["result"])

    # Get latest price history
    
    series_1, series_2 = get_latest_klines()

    # Get the zscore and confirm if hot
    if len(series_1) > 0 and len(series_2) > 0:
        # Replace last kline price with latest orderbook mid price
        series_1 = series_1[:-1]
        series_2 = series_2[:-1]
        series_1.append(mid_price_1)
        series_2.append(mid_price_2)

        _, zscore_list = calculate_metrics(series_1, series_2)

        zscore = zscore_list[-1]
        if zscore > 0:
            signal_sign_positive = True
        else:
            signal_sign_positive = False

        return (zscore, signal_sign_positive)

    return 


            


get_latest_zscore()




    


    