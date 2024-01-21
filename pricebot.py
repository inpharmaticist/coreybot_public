#!/usr/bin/python

import sys
import json
import os
import datetime

#Load and parse config
config=json.loads(open('bot.conf', "r").read())
signalacct=config['signalacct']
destination=config['signalcontacts'][sys.argv[1]]
pricefile=config['pricehistory']
priceloaded=open(pricefile, "r").read()
prices=json.loads(priceloaded)
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

#Update price history with current price (replaces today's with now).
prices.update({datetime.datetime.now().strftime('%Y%m%d'):currentprice})

#Keep history to 200 days
while True:
    if len(prices) <= 200:
        break
    leastdate=today
    del prices[min(prices)]

#Update price history file
if not prices==json.loads(priceloaded):
    updateprices = open(pricefile, "w")
    updateprices.write(json.dumps(prices))
    updateprices.close

#Get Mayer Multiple. This is the current price over the 200 day moving average.
ma200=0
for price in prices.values():
    ma200=ma200+price
ma200=ma200/len(prices)
mm=prices[max(prices)]/ma200

# Get all the things
satsperusd=100000000/float(currentprice)
block=json.loads(os.popen('curl -sSL "'+mempoolinstance+'/api/blocks/tip/height"').read())
balance_prep=json.loads(os.popen('bitcoin-cli -rpcwallet=cormorant getbalance').read())
budget=float(balance_prep)*100000000/5
balance=balance_prep*100000000
recfees=json.loads(os.popen('curl -sSL '+mempoolinstance+'/api/v1/fees/recommended').read())
fastestFee=recfees['fastestFee']
halfHourFee=recfees['halfHourFee']
hourFee=recfees['hourFee']
economyFee=recfees['economyFee']
minimumFee=recfees['minimumFee']
unconfirmedcount=json.loads(os.popen('curl -sSL "'+mempoolinstance+'/api/mempool"').read())
halving=datetime.datetime.now() + (840000-block)*datetime.timedelta(minutes=10)
halving=halving.strftime('%x %H:%M')
epoch=divmod(block,210000)[0]
mining_period=divmod(block-epoch*210000,2016)[0]
block_num=divmod(block,2016)[1]
timechain=str(epoch+1)+'/'+str(mining_period+1)+'/'+str(block_num+1)

message="""***Blockheight:
"""+str(block)+""" aka """+str(timechain)+"""

***Fiat:
\$"""+f"{currentprice:,.2f}"+"""/BTC
"""+str(int(satsperusd))+""" sats/$
Mayer Multiple """+f"{mm:,.2f}"+"""

***Mempool:
Unconfirmed
"""+f"{unconfirmedcount['count']:,}"+""" tx

Fees in sat/vbyte by priority
<"""+str(minimumFee)+""" Purging
"""+str(economyFee)+""" None
"""+str(hourFee)+""" Low
"""+str(halfHourFee)+""" Medium
"""+str(fastestFee)+""" High

***Halving Party:
Est. Date: """+str(halving)+"""
Price:
\$"""+f"{currentprice/10:,.2f}"+""" Founder
\$"""+f"{currentprice/20:,.2f}"+""" Member
Treasury:
"""+f'{round(balance):,}'+""" sats
Budget:
"""+f'{budget:,.0f}'+""" sats
\$"""+f"{currentprice*balance_prep/5:,.2f}"

os.system('signal-cli -a '+signalacct+' send -m "'+message+'" '+destination)

