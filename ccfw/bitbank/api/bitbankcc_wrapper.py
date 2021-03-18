# -*- coding: utf-8 -*-
# author:melonTai
# description:util stats

import python_bitbankcc
from ... import utils_

def get_balance(value, name):
    for item in value['assets']:
        if item['asset'] == name:
            return {'onhand':utils_.round_down(item['onhand_amount']), 'free':utils_.round_down(item['free_amount'])}
    raise ValueError('assets does not include {} asset'.format(name))

def get_eff_quote(amount, symbol):
    pub = python_bitbankcc.public()
    board = pub.get_depth(symbol)
    # board['bids'].sort(key = lambda x : float(x[0]))
    # board['asks'].sort(key = lambda x : float(x[0]), reverse=True)
    # 実効ASK計算
    i = 0
    s = 0
    while s <= amount:
        s += float(board['asks'][i][1])
        i += 1

    # 実効BID計算
    j = 0
    t = 0
    while t <= amount:
        t += float(board['bids'][j][1])
        j += 1

    return float(board['bids'][i-1][0]), float(board['asks'][j-1][0])
