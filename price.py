#!/usr/bin/python

import sys
import json
import os
import datetime

def price():
    #Load and parse config
    config_prep=open('/home/user/Desktop/scripts/coreybot/bot.conf', "r")
    config=json.loads(config_prep.read())
    config_prep.close
    # signalacct=config['signalacct']

    pricefile=config['pricehistory']
    priceloaded=open(pricefile, "r")
    pricesog=json.loads(priceloaded.read())
    mempoolinstance=config['mempool']

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

    today=datetime.datetime.now().strftime('%Y%m%d')    

    prices=pricesog
    #Update price history with current price (replaces today's with now).
    prices.update({datetime.datetime.now().strftime('%Y%m%d'):currentprice})

    #Keep history to 200 days
    while True:
        if len(pricesog) <= 200:
            break
        leastdate=today
        del prices[min(prices)]

    #Create price history backup
    createbackup=open(pricefile+str(datetime.datetime.now()), "w")
    createbackup.write(json.dumps(prices,indent=3))
    createbackup.close

    #Update price history file
    if not prices==pricesog:
        updateprices = open(pricefile, "w")
        updateprices.write(json.dumps(prices,indent=3))
        updateprices.close

    #Get Mayer Multiple. This is the current price over the 200 day moving average.
    ma200=0
    for price in prices.values():
        ma200=ma200+price
    ma200=ma200/len(prices)
    mm=prices[max(prices)]/ma200

    # Get all the things
    satsperusd=100000000/float(currentprice)

    message="""\$"""+f"{currentprice:,.2f}"+"""/BTC
"""+str(int(satsperusd))+""" sats/$
Mayer Multiple """+f"{mm:,.2f}"

    return message
