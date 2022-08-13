# api

from pybit import usdt_perpetual
from pybit import HTTP
from time import sleep


# config

mode = "test"
timeframe = 60
kline_limit = 200
z_score_window = 21


# live api

api_key_mainnet = ""
api_secret_mainnet = ""


# test API
api_key_testnet = "NxHj88GUceVJNGQiUL"
api_secret_testnet = "6EwFeftts97jarOxwK1pbAsWm0ckvdOAsz73"


# selected api
api_key = api_key_testnet if mode == "test" else api_key_mainnet
api_secret = api_secret_testnet if mode == "test" else api_secret_testnet

# selected URL
api_url = "https://api-testnet.bybit.com" if mode == "test" else "https://api.bybit.com"


# session activation
session = usdt_perpetual.HTTP(
    endpoint=api_url
    )

# websocket connection
# session_unauth = inverse_perpetual.HTTP(
#     endpoint="https://api-testnet.bybit.com"
# )
# print(session.orderbook(symbol="BTCUSD"))

# ws = websocket.WebSocketApp(
# 	"wss://stream-testnet.bybit.com/realtime"
# 	)

# ws.send('{"op":"subscribe","args":["klineV2.1.BTCUSD"]}')

ws_inverseP = usdt_perpetual.WebSocket(
    test=True,
    ping_interval=30,  # the default is 30
    ping_timeout=10,  # the default is 10
    domain="bybit"  # the default is "bybit"
)


def handle_message(msg):
    print(msg)


# To subscribe to multiple symbols,
# pass a list: ["BTCUSD", "ETHUSD"]
# ws_inverseP.orderbook_25_stream(
#     handle_message, "BTCUSD"
# )
