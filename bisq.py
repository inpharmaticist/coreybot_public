#!/usr/bin/env python

import json
import datetime
import os


def datefromts(ts):
    return datetime.datetime.utcfromtimestamp(ts).date()

def bisqinfo():
    count=0
    usd=0
    btc=0
    price=0

    #Get bitcoin price
    try:
        #Kracken price api
        #https://algotrading101.com/learn/kraken-api-guide/
        currentprice=json.loads(os.popen('curl "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"').read())
        currentprice=float(currentprice['result']['XXBTZUSD']['c'][0])
    except:
        #Coinbase price api
        currentprice=json.loads(os.popen('curl https://api.coinbase.com/v2/prices/BTC-USD/spot').read())
        currentprice=float(currentprice['data']['amount'])

    trades=json.loads(open('/home/user/Desktop/Sources/Bisq/btc_mainnet/db/trade_statistics.json', "r").read())
    yesterday=datetime.datetime.now().date()-datetime.timedelta(days=1)
    
    for trade in trades:        
        if datefromts(int(str((trade['tradeDate']-28800000))[0:10]))==yesterday and trade['currency']=='USD':
            usd=usd+trade['tradePrice']*trade['tradeAmount']/1000000000000
            btc=btc+trade['tradeAmount']/100000000
            count=count+1
    price=usd/btc

    return count,usd,btc,price,currentprice
