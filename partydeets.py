#!/usr/bin/python

import json
import os
import datetime

def partydeets():
    # #Load and parse config
    config_prep=open('/home/user/Desktop/scripts/coreybot/bot.conf', "r")
    config=json.loads(config_prep.read())
    config_prep.close
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

    block=json.loads(os.popen('curl -sSL "'+mempoolinstance+'/api/blocks/tip/height"').read())
    balance_prep=json.loads(os.popen('ssh redactrx@192.168.1.78 bitcoin-cli -rpcwallet=cormorant getbalance').read())
    budget=float(balance_prep)*100000000/5
    balance=balance_prep*100000000
    halving=datetime.datetime.now() + (840000-block)*datetime.timedelta(minutes=10)
    halving=halving.strftime('%x %H:%M')
                            
    message="""The halving party celebrates the reduction in bitcoin block rewards by 50%, which happens every ~4 years and further hardens the currency. More details here: 
https://docs.google.com/document/d/1TTF9rxNGzP5EJiYLUhsQIk9jO_21ZiHSSKRqwi0rQ08/edit#heading=h.z6ne0og04bp5

Budgetary details here: 
https://docs.google.com/document/d/1cGsoyPzc2T-d3Pfgqyh8l-f1dNbqZzTpcIqenDbl5QY/edit

Est. Date: """+str(halving)+"""
Price:
\$"""+f"{currentprice/10:,.2f}"+""" Founder
\$"""+f"{currentprice/20:,.2f}"+""" Member
Treasury:
"""+f'{round(balance):,}'+""" sats
Budget:
"""+f'{budget:,.0f}'+""" sats
\$"""+f"{currentprice*balance_prep/5:,.2f}"+"""

Help Noah with planning!
https://docs.google.com/document/d/1gMylYptWkBjCBsvOvWTj2NAdu6EvxzmXQlzheFVh2EI/edit"""

    return message
