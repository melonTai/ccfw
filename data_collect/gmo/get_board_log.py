import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import numpy as np
import pandas as pd
from pprint import pprint
import time
from datetime import datetime, timedelta
import traceback
import asyncio
from api_wrapper.gmo.realtime_stream import RealTimeBoard, RealTimeTicker
from api_wrapper.gmo.api.public import get_ticker
import logging

logger = logging.getLogger(__name__)
def get_board(symbol, board, ticker, num = 10):
    dict_data = {}
    if 'timestamp' in board:
        dict_data['time'] = board['timestamp']
    else:
        dict_data['time'] = datetime.now().timestamp()*1000
    if 'last' in ticker:
        dict_data['last'] = ticker['last']
    else:
        dict_data['last'] = get_ticker(symbol)['last']
    #print(board['asks'][0]['price'])
    asks_price = {'asks_price_{}'.format(i) : board['asks'][i]['price'] for i in range(num)}
    dict_data.update(asks_price)
    asks_size = {'asks_size_{}'.format(i) : board['asks'][i]['size'] for i in range(num)}
    dict_data.update(asks_size)
    bids_pirce = {'bids_price_{}'.format(i) : board['bids'][i]['price'] for i in range(num)}
    dict_data.update(bids_pirce)
    bids_size = {'bids_size_{}'.format(i) : board['bids'][i]['size'] for i in range(num)}
    dict_data.update(bids_size)

    return pd.Series(dict_data)

async def get_board_log(period, interval, symbol, board_ins, ticker_ins, folder_path, num = 10):
    # period:second
    start_time = datetime.now()
    end_time = start_time
    main_list = []
    while (end_time - start_time).seconds < period:

        if board_ins.board:
            try:
                dict_data = get_board(symbol, board_ins.board, ticker_ins.ticker, num)
                main_list.append(dict_data)
            except Exception as e:
                print(traceback.format_exc())
        else:
            print("no board")
        await asyncio.sleep(interval)
        end_time = datetime.now()




    df = pd.concat(main_list, axis = 1).T
    df.to_csv(
        '{folder_path}/interval_{period}sec_day{day}_start_{start_time}_end{end_time}.csv'.format(
            folder_path = folder_path,
            period = period,
            day = start_time.strftime("%Y%m%d"),
            start_time = start_time.strftime("%H%M"),
            end_time = end_time.strftime("%H%M")
        )
    )
async def main(symbol, board_ins, ticker_ins):
    init_time = datetime.now() - timedelta(days=1)
    while True:
        now = datetime.now()
        if init_time.day != now.day:
            init_time = now
            folder_path = '{OneDrive}/cryptocurrency/gmo/data/{symbol}/{year}/{month:02}/{year}_{month:02}_{day:02}'.format(
                OneDrive = os.environ['ONEDRIVE'],
                symbol = symbol,
                year = init_time.year,
                month = init_time.month,
                day = init_time.day
            )
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        try:
            print("get_start:",datetime.now())
            await get_board_log(3600, 1, symbol, board_ins, ticker_ins, folder_path)
            print("get_end:",datetime.now())
        except Exception as e:
            print(traceback.format_exc())

# メインの処理
async def run(symbol):
    board = RealTimeBoard(symbol = symbol)
    ticker = RealTimeTicker(symbol = symbol)
    try:
        await asyncio.gather(
            board.wait(),
            ticker.wait(),
            main(symbol, board, ticker)
        )
    except Exception as e:
        print(traceback.format_exc())


if __name__ == '__main__':
    import signal
    import sys
    formatter = '%(levelname)s : %(asctime)s : %(message)s'
    logging.basicConfig(level=logging.ERROR, format=formatter)
    if len(sys.argv) < 2:
        raise ValueError('not enough arguments need 1')
    symbol = sys.argv[1]
    print(symbol)
    print(type(symbol))
    asyncio.run(run(symbol))
    exit()
