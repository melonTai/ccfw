import numpy as np
import pandas as pd
import python_bitbankcc
from pprint import pprint
import time
from datetime import datetime, timedelta

def get_latest_0900():
    """
    直近の午前9時のdatetimeインスタンスを取得
    """
    now = datetime.now()
    today_0900 = datetime(now.year, now.month, now.day, 9, 0)
    yesterday_0900 = datetime(now.year, now.month, now.day - 1, 9, 0)
    latest_0900 = today_0900 if today_0900 <= now else yesterday_0900
    return latest_0900

def get_ohlcv_per_sec_in_period(symbol, period, delta):
    """
    argument
    --------
    symbol : str
        通貨ペア
        ex...etc_jpy, btc_jpy, xrp_jpy
    period : int
        過去period日間の秒速ohlcvを取得
    delta : int
        何ミリ秒間隔でohlcvを取得するか

    return
    ------
    df : pandas.DataFrame
        取得したohlcv
    """
    latest_0900 = get_latest_0900()
    ohlcv = []
    for i in reversed(range(1,period+1)):
        ohlcv += get_ohlcv_per_sec((latest_0900 - timedelta(days=i)).timestamp()*1000, delta, symbol)
    df = pd.DataFrame(ohlcv)
    return df

def get_ohlcv_per_sec(start_timestamp, delta_timestamp, symbol):
    """
    argument
    --------
    start_timestamp : float
        timestamp(msec)
    delta_timestamp : float
        timestamp(msec)
        ローソク足間隔
    """
    pub = python_bitbankcc.public()
    now = datetime.now()
    today_0900 = datetime(now.year, now.month, now.day, 9, 0)
    yesterday_0900 = datetime(now.year, now.month, now.day - 1, 9, 0)
    latest_0900 = today_0900 if today_0900 <= now else yesterday_0900
    second_latest_0900 = latest_0900 - timedelta(days = 1)
    startday = datetime.fromtimestamp(start_timestamp/1000)
    flag = False
    if latest_0900 <= startday:
        # 直近の約定履歴60個
        transactions = pub.get_transactions(symbol)
        transactions['transactions'].reverse()
        flag = True
    elif second_latest_0900 <= startday < latest_0900:
        transactions = pub.get_transactions(symbol, second_latest_0900.strftime('%Y%m%d'))
    else:
        transactions = pub.get_transactions(symbol, startday.strftime('%Y%m%d'))

    trans_size = len(transactions['transactions'])
    # print(startday)
    # print(trans_size)
    timestamp_down = start_timestamp
    timestamp_up = timestamp_down + delta_timestamp
    timestamp = transactions['transactions'][0]['executed_at']
    i = 0
    ohlcv = []
    # pprint(transactions)
    # return None

    while timestamp < timestamp_down:
        if i >= trans_size:
            break
        timestamp = transactions['transactions'][i]['executed_at']
        i += 1
    while i < trans_size:
        # print(i)
        # print(timestamp)
        # print(timestamp_down)
        # print(timestamp_up)
        data_unit = []
        ohlcv_unit = dict()
        while timestamp_down <= timestamp and timestamp < timestamp_up and i < trans_size:
            data_unit.append(transactions['transactions'][i])
            i += 1
            if i < trans_size:
                timestamp = transactions['transactions'][i]['executed_at']
        if len(data_unit) == 0:
            if len(ohlcv) == 0:
                ohlcv_unit = {'timestamp':timestamp_down,'open':np.nan, 'high':np.nan, 'low':np.nan, 'close':np.nan, 'volume':0}
            else:
                ohlcv_unit = {'timestamp':timestamp_down,'open':ohlcv[-1]['close'], 'high':ohlcv[-1]['close'], 'low':ohlcv[-1]['close'], 'close':ohlcv[-1]['close'], 'volume':0}
        else:
            ohlcv_unit['timestamp'] = timestamp_down
            ohlcv_unit['open'] = float(data_unit[0]['price'])
            ohlcv_unit['high'] = max([float(data['price']) for data in data_unit])
            ohlcv_unit['low'] = min([float(data['price']) for data in data_unit])
            ohlcv_unit['close'] = float(data_unit[-1]['price'])
            ohlcv_unit['volume'] = sum([float(data['amount']) for data in data_unit])
        ohlcv.append(ohlcv_unit)
        timestamp_down = timestamp_up
        timestamp_up += delta_timestamp
    if flag:
        while now.timestamp()*1000 > timestamp_down:
            if len(ohlcv) == 0:
                ohlcv_unit = {'timestamp':timestamp_down,'open':np.nan, 'high':np.nan, 'low':np.nan, 'close':np.nan, 'volume':0}
            else:
                ohlcv_unit = {'timestamp':timestamp_down,'open':ohlcv[-1]['close'], 'high':ohlcv[-1]['close'], 'low':ohlcv[-1]['close'], 'close':ohlcv[-1]['close'], 'volume':0}
            ohlcv.append(ohlcv_unit)
            timestamp_down += delta_timestamp

    return ohlcv

if __name__ == '__main__':
    df = get_ohlcv_per_sec_in_period('xrp_jpy', 3, 1000)
    df.to_csv('data.csv')
