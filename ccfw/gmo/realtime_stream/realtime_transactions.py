# -*- coding: utf-8 -*-
# author:tamelon
# description:bitbank scalping
import logging
import asyncio
from pprint import pprint
import traceback
import sys
import signal
import time
import os
import json
from . import RealTimeBase
from datetime import datetime

class RealTimeTransactions(RealTimeBase):
    def __init__(self, **kargs):
        self.transactions = []
        super().__init__(**kargs)

    async def on_connect(self, _ws):
        trans_msg = {
        "command": "subscribe",
        "channel": "trades",
        "symbol": self.symbol
        }
        await _ws.send(json.dumps(trans_msg))
        await super().on_connect(_ws)

    async def on_message(self, data):
        data = json.loads(data)
        if 'channel' in data.keys() and data['channel'] == 'trades':
            self.transactions = self.__reformat(data)
        await super().on_message(data)

    def __reformat(self, data):
        transactions = {}
        for key in data.keys():
            if key in ['price', 'size']:
                transactions[key] = float(data[key])
            elif key == 'timestamp':
                transactions[key] = datetime.strptime(
                    data['timestamp'],'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()*1000#ミリ秒
            else:
                transactions[key] = data[key]
        return transactions
