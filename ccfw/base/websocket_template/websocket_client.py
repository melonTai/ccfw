# -*- coding: utf-8 -*-
# author:tamelon
# description:websocket template
import logging
import asyncio
from pprint import pprint
import traceback
import sys
import signal
import time
import os
import json
import websockets

class WebsocketClient(object):
    # connectイベント時のハンドラ
    async def on_connect(self, _ws):
        self.logger.info('connected to server')

    # disconnectイベント時のハンドラ
    async def on_disconnect(self):
        self.logger.info('disconnected from server')

    # messageイベント時のハンドラ
    async def on_message(self, data):
        self.logger.info('Received message %s')

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ws_ = None

    async def wait(self):
        try:
            while True:
                try:
                    async with websockets.connect(self.endpoint) as ws:
                        await self.on_connect(ws)
                        while True:
                            try:
                                data = await ws.recv()
                                await self.on_message(data)
                            except Exception as e:
                                self.logger.error(traceback.format_exc())
                    await self.on_disconnect()
                except Exception as e:
                    self.logger.error(traceback.format_exc())
                    self.logger.error('try recconect')
        except Exception as e:
            self.logger.error(traceback.format_exc())
