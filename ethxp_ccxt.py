# -*- coding: utf-8 -*-

# Libraries
import ccxt

print(ccxt.exchanges) # print a list of all available exchange classes

deribit = ccxt.deribit()
deribit_markets = deribit.load_markets()


print(deribit.id, deribit.load_markets())
print(deribit.fetch_ticker('BTC-IBUT-29SEP23-5000_22000_80000'))
print(deribit.fetch_order_book(deribit.symbols[0]))
