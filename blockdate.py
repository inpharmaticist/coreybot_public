#!/usr/bin/python

import json
import os
from bisq import bisqinfo 

def blockdate():
    #Load and parse config
    config_prep=open('/home/user/Desktop/scripts/coreybot/bot.conf', "r")
    config=json.loads(config_prep.read())
    config_prep.close
    mempoolinstance=config['mempool']

    # Get all the things
    block=json.loads(os.popen('curl -sSL "'+mempoolinstance+'/api/blocks/tip/height"').read())
    epoch=divmod(block,210000)[0]

    mining_period=divmod(block,2016)[0]-divmod(epoch*210000,2016)[0]
    block_num=divmod(block,2016)[1]
    timechain=str(epoch+1)+'/'+str(mining_period)+'/'+str(block_num+1)

    message=str(block)+""" aka """+str(timechain)

    return message
