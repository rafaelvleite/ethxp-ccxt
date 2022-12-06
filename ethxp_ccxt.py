# -*- coding: utf-8 -*-

# Libraries
import ccxt

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
