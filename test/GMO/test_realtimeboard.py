import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from api_wrapper.gmo.realtime_stream import RealTimeBoard, RealTimeTicker, RealTimeTransactions
import asyncio
import traceback
from pprint import pprint

async def watch(board, ticker, transactions):
    while True:
        if board.board:
            print(board.board['asks'][0]['price'])
        if ticker.ticker:
            print(ticker.ticker)
        if transactions.transactions:
            print(transactions.transactions)
        await asyncio.sleep(1)
async def run():
    board = RealTimeBoard(symbol = 'XRP_JPY')
    ticker = RealTimeTicker(symbol = 'XRP_JPY')
    transactions = RealTimeTransactions(symbol = 'XRP_JPY')
    await asyncio.gather(
        board.wait(),
        ticker.wait(),
        transactions.wait(),
        watch(board, ticker, transactions)
    )


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    import logging

    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
    exit()
