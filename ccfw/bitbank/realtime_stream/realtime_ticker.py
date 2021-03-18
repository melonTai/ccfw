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
from ... import utils_

class RealTimeTicker(RealTimeBase):
    def __init__(self,**kargs):
        self.ticker = {}
        super().__init__(**kargs)

    # 接続時、板情報とその差分配信チャンネルに入室
    async def on_connect(self):
        await self.sio_.emit('join-room','ticker_{}'.format(self.symbol))
        await super().on_connect()

    # 情報取得時板情報更新
    async def on_message(self, data):
        if data['room_name'] == 'ticker_{}'.format(self.symbol):
            self.ticker = {
                key : utils_.round_down(value)
                if isinstance(value, str) else value
                for key, value in data['message']['data'].items()
            }
        await super().on_message(data)
