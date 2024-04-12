#!/usr/bin/env python

import json
import os
import time
import datetime
import partydeets
import price
import bisq
import blockdate

def system(cmd):
    os.system(cmd)

def readsys(cmd):
    os.popen(cmd).read()

## The following was supposed to be a manual cron, but I got ecron working so never mind.
# coreybotdata = open('coreybot.txt', "r").read()
# coreybotdata=json.loads(coreybotdata)
# maga=datetime.datetime.strptime(coreybotdata['maga'], '%Y-%m-%d %H:%M:%S')
# encinitas=datetime.datetime.strptime(coreybotdata['encinitas'], '%Y-%m-%d %H:%M:%S')
# now=datetime.datetime.now()
# if maga.date() < now.date() and now.time() > datetime.datetime.strptime('08:00', '%H:%M').time():
#     print('morning')
# elif maga.time() < datetime.datetime.strptime('20:00', '%H:%M').time() and now.time() >= datetime.datetime.strptime('20:00', '%H:%M').time():
#     print('evening')
# else:
#     print('neither')


ip='192.168.1.78'
mempool='http://'+ip+':4080'
block=json.loads(os.popen('curl -sSL "'+mempool+'/api/blocks/tip/height"').read())
signalacct='+16196637097'

countdowntarget=840000
countdownlist=[831500,832000,832500,833000,833500,834000,834500,835000,835500,836000,836500,837000,837500,838000,838500,839000,839100,839200,839300,839400,839500,839600,839700,839800
,839900,839906,839912,839918,839924,839930,839936,839942,839948,839954,839960,839966,839972,839978,839984,839990,839991,839992,839993,839994,839995,839996,839997,839998
,839999,840000,835102]

halvingtreasury=os.popen('ssh redactrx@'+ip+' bitcoin-cli -rpcwallet=cormorant getbalance').read()

while True:

    try:
        blockupdate=json.loads(os.popen('curl -sSL "'+mempool+'/api/blocks/tip/height"').read())
    except:
        system('nmcli radio wifi off && nmcli radio wifi on')
        blockupdate=0
    if blockupdate > block:
        block=blockupdate
        if block in countdownlist:
            blockstats=json.loads(os.popen('ssh redactrx@'+ip+' bitcoin-cli getblockstats '+str(block)).read())
            subsidy=blockstats['subsidy']
            if block == countdowntarget-1:
                line2='1 block to go!'
            elif block == countdowntarget:
                line2='🎉 We made it! 🍻'
            else:
                line2=f"{countdowntarget-block:,}"+' blocks to go!'

            message="""Block height """+f"{block:,}"+"""
"""+line2+"""
Block subsidy """+f"{subsidy:,}"+""" sats"""
            system("""signal-cli -a """+signalacct+""" send -m '"""+message+"""'  -g mbCXDUlhOPnl1MLmA0q348cotwB30CQ+Ej8pORkdDHg=""")
            system("""signal-cli -a """+signalacct+""" send -m '"""+message+"""'  -g bMyNap7f/SxD7QSSNyS+W8xSRYabhrhZ4V3ddmu3GCo=""")

    try:
        halvingtreasuryupdate=float(os.popen('ssh redactrx@'+ip+' bitcoin-cli -rpcwallet=cormorant getbalance').read().replace('\n',''))
    except:
        pass
    if float(halvingtreasuryupdate) > float(halvingtreasury) and halvingtreasuryupdate != '':
        system('signal-cli -a '+signalacct+' send -m "Funds have been added to the Halving Party treasury! Balance is now '+str(halvingtreasuryupdate)+' BTC" -g mbCXDUlhOPnl1MLmA0q348cotwB30CQ+Ej8pORkdDHg=')
        system('signal-cli -a '+signalacct+' send -m "Funds have been added to the Halving Party treasury! Balance is now '+str(halvingtreasuryupdate)+' BTC" -g D7/DcL5+8ZDyajrqYIBQfa33qdjNUuTaxHtY7VvCTcQ=')
        system('signal-cli -a '+signalacct+' send -m "Funds have been added to the Halving Party treasury! Balance is now '+str(halvingtreasuryupdate)+' BTC" -g bMyNap7f/SxD7QSSNyS+W8xSRYabhrhZ4V3ddmu3GCo=')
        halvingtreasury=halvingtreasuryupdate
    elif float(halvingtreasuryupdate) < float(halvingtreasury) and halvingtreasuryupdate != '':
        system('signal-cli -a '+signalacct+' send -m "Funds have been spent from the Halving Party treasury. Balance is now '+str(halvingtreasuryupdate)+' BTC" -g mbCXDUlhOPnl1MLmA0q348cotwB30CQ+Ej8pORkdDHg=')
        system('signal-cli -a '+signalacct+' send -m "Funds have been spent from the Halving Party treasury. Balance is now '+str(halvingtreasuryupdate)+' BTC" -g D7/DcL5+8ZDyajrqYIBQfa33qdjNUuTaxHtY7VvCTcQ=')
        system('signal-cli -a '+signalacct+' send -m "Funds have been spent from the Halving Party treasury. Balance is now '+str(halvingtreasuryupdate)+' BTC" -g bMyNap7f/SxD7QSSNyS+W8xSRYabhrhZ4V3ddmu3GCo=')
        halvingtreasury=halvingtreasuryupdate

    try:
        messages=os.popen('signal-cli -a '+signalacct+' receive').read()
    except:
        message=''

    parsed=[]
    single={}
    for line in messages.splitlines():
        if line[0:14] == 'Envelope from:':
            atgroup = False
            atmentions = False
            if len(single) > 0:
                parsed.append(single)
                single={}
            single.update({'mentioned':False})
            single.update({'from':line[14:]})
        elif line[0:10] == 'Timestamp:':
            single.update({'timestamp':line[11:]})
        elif line[0:5] == 'Body:':
            single.update({'body':line[6:]})
            for bodyword in line:
                if bodyword[0:9] == '@coreybot':
                    single.update({'mentioned':True})
        elif line[0:11] == 'Group info:':
            atgroup = True
        elif line[0:5] == '  Id:' and atgroup:
            single.update({'groupid':line[6:]})
        elif line[0:7] == '  Name:' and atgroup:
            single.update({'groupname':line[8:]})
        elif line[0:9] == 'Mentions:':
            atmentions = True
        elif len(line.split()) >= 3 and atmentions:
            if line.split()[2] == signalacct+':':
                single.update({'mentioned':True})

    if len(single) > 0:
        parsed.append(single)

    for message in parsed:
        # saved=open('savedmessages.txt', "a")
        # saved.write(json.dumps(message,indent=3))

        for term in message['from'].split():
            if term[0:1]=='+':
                author=term
                break
        if message['mentioned']==True:
            recognized=False
            for word in message['body'].split():
                if word[0:11]=='blockheight':
                    recognized=True
                    response=blockdate.blockdate()
                    system('signal-cli -a '+signalacct+' send -m "'+response+'" --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
                elif word[0:6]=='stock':
                    system('signal-cli -a '+signalacct+' send -m "Oof, gimme a min, my dude." --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
                    gettxoutsetinfo= os.popen('ssh redactrx@'+ip+' bitcoin-cli gettxoutsetinfo').read()
                    gettxoutsetinfo=(json.loads(gettxoutsetinfo))
                    blockheight=str(gettxoutsetinfo['height'])
                    stock=gettxoutsetinfo['total_amount']
                    stock= '{:,}'.format(stock)
                    recognized=True
                    system('signal-cli -a '+signalacct+' send -m "As of block '+blockheight+' the total bitcoin issued is '+stock+'." --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
                elif word[0:12] == 'partyaddress':
                    partyaddress=os.popen('ssh redactrx@'+ip+' bitcoin-cli -rpcwallet=cormorant getnewaddress').read()
                    recognized=True
                    system('signal-cli -a '+signalacct+' send -m "This address is for you and you only to send your funds for the halving party, welcome to the Elite Bitcoiners! \n\n'+partyaddress+'\n\nhttps://mempool.space/address/'+partyaddress+'" --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
                    usedaddresses = open('/home/user/Desktop/scripts/coreybot/addresses.txt', "r").read()
                    usedaddresses=json.loads(usedaddresses)
                    try:
                        usedaddresses[author].update({str(datetime.datetime.now()):partyaddress})
                    except:
                        usedaddresses.update({author:{str(datetime.datetime.now()):partyaddress}})                    
                    write=open('/home/user/Desktop/scripts/coreybot/addresses.txt', "w")
                    write.write(json.dumps(usedaddresses,indent=3))
                    write.close
                elif word[0:10]=='partydeets':
                    recognized=True
                    response=partydeets.partydeets()
                    system('signal-cli -a '+signalacct+' send -m "'+response+'" --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
                elif word[0:8]=='booklist':
                    recognized=True
                    booklist_prep=open('/home/user/Desktop/scripts/coreybot/booklist', "r").read()
                    booklist=booklist_prep
                    # booklist_prep.close
                    system('signal-cli -a '+signalacct+' send -m "'+booklist+'" --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
                elif word[0:5]=='price':
                    recognized=True
                    response=price.price()
                    system('signal-cli -a '+signalacct+' send -m "'+response+'" --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
                elif word[0:4]=='bisq':
                    recognized=True
                    bisqcount,bisqusd,bisqbtc,bisqprice,currentprice=bisq.bisqinfo()
                    response=str(bisqcount)+""" trades
\$"""+f"{bisqusd:,.2f}"+"""
"""+f"{bisqbtc:,.8f}"+""" BTC
\$"""+f"{bisqprice:,.2f}"+"""/BTC
Surveillance discount """+f"{100*(bisqprice/currentprice-1):,.1f}"+"""%"""
                    system('signal-cli -a '+signalacct+' send -m "'+response+'" --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
            if recognized==False:
                system('signal-cli -a '+signalacct+' send -m "Didn\'t catch that, jefe. I currently recognize the following commands:\n-blockheight\n-stock\n-partyaddress\n-partydeets\n-booklist\n-price\n-bisq" --quote-author '+author+' --quote-timestamp '+message['timestamp'].split()[0]+' -g '+message['groupid'])
    # saved.close
    time.sleep(10)
    # print(json.dumps(parsed,indent=3))

            
