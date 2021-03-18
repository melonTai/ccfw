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
from . import RealTimeBase
import json
from datetime import datetime

class RealTimeTicker(RealTimeBase):
    def __init__(self,**kargs):
        self.ticker = {}
        super().__init__(**kargs)

    async def on_connect(self, _ws):
        ticker_msg = {
        "command": "subscribe",
        "channel": "ticker",
        "symbol": self.symbol
        }
        await _ws.send(json.dumps(ticker_msg))
        await super().on_connect(_ws)

    async def on_message(self, data):
        data = json.loads(data)
        if 'channel' in data.keys() and data['channel'] == 'ticker':
            self.ticker = self.__reformat(data)
        await super().on_message(data)

    def __reformat(self, data):
        ticker = {}
        for key in data.keys():
            if key in ['ask', 'bid', 'high', 'low', 'last', 'volume']:
                ticker[key] = float(data[key])
            elif key == 'timestamp':
                ticker[key] = datetime.strptime(
                    data['timestamp'],'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()*1000#ミリ秒
            else:
                ticker[key] = data[key]
        return ticker
