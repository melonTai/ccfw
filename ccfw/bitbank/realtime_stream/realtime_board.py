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

class RealTimeBoard(RealTimeBase):
    def __init__(self, **kargs):
        self.board = []
        self.diff = []
        super().__init__(**kargs)

    # 接続時、板情報とその差分配信チャンネルに入室
    async def on_connect(self):
        await self.sio_.emit('join-room','depth_whole_{}'.format(self.symbol))
        await self.sio_.emit('join-room','depth_diff_{}'.format(self.symbol))
        await super().on_connect()

    # 情報取得時板情報更新
    async def on_message(self, data):
        if data['room_name'] == 'depth_whole_{}'.format(self.symbol):
            self.board = self.reformat_board(data['message']['data'])
        elif data['room_name'] == 'depth_diff_{}'.format(self.symbol):
            self.diff = self.reformat_board(data['message']['data'])
            self.board = self.update_board(self.diff, self.board)
        await super().on_message(data)

    # dataの値を文字列からutils_.round_downに変換
    def reformat_board(self, data):
        board = {'asks': [], 'bids': [], 'timestamp':0}
        for key in data.keys():
            if key in ['asks', 'bids']:
                board[key] = [{'price':utils_.round_down(quote[0]), 'size': utils_.round_down(quote[1])} for quote in data[key]]
            elif key == 'a':
                board['asks'] = [{'price':utils_.round_down(quote[0]), 'size': utils_.round_down(quote[1])} for quote in data['a']]
            elif key == 'b':
                board['bids'] = [{'price':utils_.round_down(quote[0]), 'size': utils_.round_down(quote[1])} for quote in data['b']]
            elif key == 'timestamp':
                board['timestamp'] = data['timestamp']
            elif key == 't':
                board['timestamp'] = data['t']
        return board

    # 板情報を更新
    def update_board(self, diff, board):
        for key in diff.keys():
            if key == 'timestamp':
                board[key] = diff[key]
            elif key in ['bids', 'asks']:
                for quote in diff[key]:
                    price_list = [quote['price'] for quote in board[key]]
                    price = quote['price']
                    size = quote['size']
                    if price in price_list:
                        if size == 0.0:
                            # delete
                            del board[key][price_list.index(price)]
                        else:
                            # update
                            board[key][price_list.index(price)]['size'] = size
                    else:
                        if size > 0.0:
                            # insert
                            board[key].append(quote)

                # sort
                if key == 'asks':
                    board[key] = sorted(board[key], key=lambda x: x['price'])
                elif key == 'bids':
                    board[key] = sorted(board[key], key=lambda x: -x['price'])

        return board
