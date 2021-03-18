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

class RealTimeTransactions(RealTimeBase):
    def __init__(self, **kargs):
        self.transactions = []
        super().__init__(**kargs)

    # 接続時、板情報とその差分配信チャンネルに入室
    async def on_connect(self):
        await self.sio_.emit('join-room','transactions_{}'.format(self.symbol))
        await super().on_connect()

    # 情報取得時板情報更新
    async def on_message(self, data):
        if data['room_name'] == 'transactions_{}'.format(self.symbol):
            self.transactions = data['message']['data']
        await super().on_message(data)
