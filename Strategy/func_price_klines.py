# interval: 60, "D"
# from: integer from timestamp in seconds
# limit: max size of 200


from config_strategy_api import session
from config_strategy_api import timeframe
from config_strategy_api import kline_limit
import datetime
import time
 
# get start times

time_start_date = 0
if timeframe == 60:
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
if timeframe == "D":
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)
time_start_seconds = int(time_start_date.timestamp())
print(time_start_seconds)

# Get historical prices (klines)
def get_price_klines(symbol_name):
    prices = session.query_mark_price_kline(
        symbol = symbol_name,
        interval = timeframe,
        limit = kline_limit,
        from_time = time_start_seconds
    )

    time.sleep(0.1)

    if len(prices["result"]) != kline_limit:
        return []
    return prices["result"]