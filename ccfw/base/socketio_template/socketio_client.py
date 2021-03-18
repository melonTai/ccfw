# -*- coding: utf-8 -*-
# author:tamelon
# description:socketio template
import socketio
import logging
import asyncio
from pprint import pprint
import traceback
import sys
import signal
import time
import os

# SocketIOのテンプレート
class SocketIOClient(object):
    # namespaceの設定用クラス
    class NamespaceClass(socketio.AsyncClientNamespace):
        async def on_connect(self):
            pass
        async def on_disconnect(self):
            pass
        async def on_message(self, data):
            pass

    # connectイベント時のハンドラ
    async def on_connect(self):
        self.logger.debug('connected to server')
        self.is_connect = True

    # disconnectイベント時のハンドラ
    async def on_disconnect(self):
        self.logger.debug('disconnected from server')
        self.is_connect = False

    # messageイベント時のハンドラ
    async def on_message(self, data):
        self.logger.debug('Received message %s', str(data))

    # Namespaceクラス内の各ハンドラをオーバーライド
    def overload_event(self):
        self.Namespace.on_connect          = self.on_connect
        self.Namespace.on_disconnect       = self.on_disconnect
        self.Namespace.on_message          = self.on_message

    # 初期化
    def __init__(
        self, endpoint,
        transports = ['websocket'], reconnection = True,
        reconnection_attempts = 0, reconnection_delay=0.1,
        reconnection_delay_max=0.5, logger=False, headers=None, namespace = '/', **kwargs):

        """
        logger_level : str
            CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.is_connect = False
        self.endpoint = endpoint
        self.transports = transports
        self.headers = headers
        self.namespace  = namespace
        self.sio_ = socketio.AsyncClient(
            reconnection = reconnection,
            reconnection_attempts = reconnection_attempts,
            reconnection_delay = reconnection_delay,
            reconnection_delay_max = reconnection_delay_max,
            logger = logger
        )
        self.Namespace   = self.NamespaceClass(self.namespace)
        self.overload_event()
        self.sio_.register_namespace(self.Namespace)

        super().__init__(**kwargs)

    # 接続
    async def connect(self):
        try:
            await self.sio_.connect(
                self.endpoint,
                namespaces = self.namespace,
                transports = self.transports
            )
        except Exception:
            self.logger.error('Cannot connect to server')
            self.logger.error(traceback.format_exc())
        # else:
        #     if not self.is_connect:
        #         self.logger.error('Namespace may be invalid.(namespace="%s")',\
        #                       self.namespace)
    # 切断
    async def disconnect(self):
        try:
            await self.sio_.disconnect()
        except Exception:
            self.logger.error('Cannot disconnect from server')
            self.logger.error(traceback.format_exc())
        else:
            self.is_connect = False

    # 再接続
    async def reconnect(self):
        await self.disconnect()
        await asyncio.sleep(5)
        await self.connect()

    # メインの処理
    async def wait(self):
        while True:
            try:
                await self.connect()
                await self.sio_.wait()
            except ValueError as e:
                if e == "Client is not in a disconnected state":
                    self.logger.error(traceback.format_exc())
                    await self.disconnect()
                    await asyncio.sleep(1)
                else:
                    raise ValueError(e)
            except RuntimeError:
                self.logger.error(traceback.format_exc())
                await self.disconnect()
                await asyncio.sleep(1)
