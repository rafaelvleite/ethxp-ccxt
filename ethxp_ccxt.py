# -*- coding: utf-8 -*-

# Libraries
import ccxt
import os
from pathlib import Path

import sys
import csv

# -----------------------------------------------------------------------------

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(''))))
sys.path.append(root + '/python')


def retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
    num_retries = 0
    try:
        num_retries += 1
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        # print('Fetched', len(ohlcv), symbol, 'candles from', exchange.iso8601 (ohlcv[0][0]), 'to', exchange.iso8601 (ohlcv[-1][0]))
        return ohlcv
    except Exception:
        if num_retries > max_retries:
            raise  # Exception('Failed to fetch', timeframe, symbol, 'OHLCV in', max_retries, 'attempts')


def scrape_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
    earliest_timestamp = exchange.milliseconds()
    timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    timedelta = limit * timeframe_duration_in_ms
    all_ohlcv = []
    while True:
        fetch_since = earliest_timestamp - timedelta
        ohlcv = retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, fetch_since, limit)
        # if we have reached the beginning of history
        if ohlcv[0][0] >= earliest_timestamp:
            break
        earliest_timestamp = ohlcv[0][0]
        all_ohlcv = ohlcv + all_ohlcv
        print(len(all_ohlcv), symbol, 'candles in total from', exchange.iso8601(all_ohlcv[0][0]), 'to', exchange.iso8601(all_ohlcv[-1][0]))
        # if we have reached the checkpoint
        if fetch_since < since:
            break
    return all_ohlcv



def write_to_csv(filename, exchange, data):
    p = Path("./data/raw/", str(exchange))
    p.mkdir(parents=True, exist_ok=True)
    full_path = p / str(filename)
    with Path(full_path).open('w+', newline='') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(data)

def scrape_candles_to_csv(filename, exchange_id, max_retries, symbol, timeframe, since, limit):
    # instantiate the exchange by id
    exchange = getattr(ccxt, exchange_id)({
        'enableRateLimit': True,  # required by the Manual
    })
    # convert since from string to milliseconds integer if needed
    if isinstance(since, str):
        since = exchange.parse8601(since)
    # preload all markets from the exchange
    exchange.load_markets()
    # fetch all candles
    ohlcv = scrape_ohlcv(exchange, max_retries, symbol, timeframe, since, limit)
    # save them to csv file
    write_to_csv(filename, exchange, ohlcv)
    print('Saved', len(ohlcv), 'candles from', exchange.iso8601(ohlcv[0][0]), 'to', exchange.iso8601(ohlcv[-1][0]), 'to', filename)


print(ccxt.exchanges) # print a list of all available exchange classes

deribit = ccxt.deribit()
deribit_markets = deribit.load_markets()

bitfinex = ccxt.bitfinex()
bitfinex_markets = bitfinex.load_markets()

bitmex = ccxt.bitmex()
bitmex_markets = bitmex.load_markets()

okx = ccxt.okx()
okx_markets = okx.load_markets()

bybit = ccxt.bybit()
bybit_markets = bybit.load_markets()

binance = ccxt.binance()
binance_markets = binance.load_markets()

"""
print(deribit.id, deribit.load_markets())
print(deribit.fetch_ticker('BTC-IBUT-29SEP23-5000_22000_80000'))
print(deribit.fetch_order_book(deribit.symbols[0]))

print(bitfinex.id, bitfinex.load_markets())
print(bitfinex.fetch_ticker('SANDF0/USTF0'))
print(bitfinex.fetch_order_book(bitfinex.symbols[0]))

print(bitmex.id, bitmex.load_markets())
print(bitmex.fetch_ticker('LTC/USDT:USDT'))
print(bitmex.fetch_order_book(bitmex.symbols[-1]))

print(okx.id, okx.load_markets())
print(okx.fetch_ticker('BTC-USD-230929-120000-P'))
print(okx.fetch_order_book(okx.symbols[0]))

print(bybit.id, bybit.load_markets())
print(bybit.fetch_ticker('10000NFT/USDT:USDT'))
print(bybit.fetch_order_book(bybit.symbols[0]))

print(binance.id, binance.load_markets())
print(binance.fetch_ticker('GO/BNB'))
print(binance.fetch_order_book(binance.symbols[0]))
"""


scrape_candles_to_csv('btc_usdt_1m.csv', 'binance', 3, 'BTC/USDT', '1m', '2017-01-0100:00:00Z', 1000)


