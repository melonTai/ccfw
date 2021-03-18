# -*- coding: utf-8 -*-
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

class RealTimeBoard(RealTimeBase):
    def __init__(self, **kargs):
        self.board = []
        self.diff = []
        super().__init__(**kargs)

    async def on_connect(self, _ws):
        board_msg = {
        "command": "subscribe",
        "channel": "orderbooks",
        "symbol": self.symbol
        }
        await _ws.send(json.dumps(board_msg))
        await super().on_connect(_ws)

    async def on_message(self, data):
        data = json.loads(data)
        if 'channel' in data.keys() and data['channel'] == 'orderbooks':
            self.board = self.__reformat(data)
        await super().on_message(data)

    def __reformat(self, data):
        board = {}
        for key in data.keys():
            if key in ['asks', 'bids']:
                board[key] = [
                    {'price': float(quote['price']), 'size': float(quote['size'])}
                    for quote in data[key]
                ]
            elif key == 'timestamp':
                board['timestamp'] = datetime.strptime(
                    data['timestamp'],'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()*1000#ミリ秒
            else:
                board[key] = data[key]
        return board
