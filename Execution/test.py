from config_execution import signal_negative_ticker
from config_execution import signal_positive_ticker
from config_execution import session
from func_position_calls import open_position_confirmation
from func_position_calls import active_position_confirmation
from func_execution_calls import set_leverage
from func_price_calls import get_ticker_trade_liquidity
# from time import sleep
# from pybit import usdt_perpetual
# ws_linear = usdt_perpetual.WebSocket(
#     test=True,
#     ping_interval=30,  # the default is 30
#     ping_timeout=10,  # the default is 10
#     domain="bybit"  # the default is "bybit"
# )
# def handle_message(msg):
#     print(msg["data"])
# # To subscribe to multiple symbols,
# # pass a list: ["BTCUSDT", "ETHUSDT"]
# ws_linear.orderbook_25_stream(
#     handle_message, "BALUSDT"
# )
# while True:
#     sleep(1)

# from pybit import usdt_perpetual
# session_unauth = usdt_perpetual.HTTP(
#     endpoint="https://api-testnet.bybit.com"
# )
# print(session_unauth.query_mark_price_kline(
#     symbol="BTCUSDT",
#     interval=1,
#     limit=2,
#     from_time=1581231260
# ))

print(session.public_trading_records(
        symbol="BTCUSDT",
        limit = 500
    ))
