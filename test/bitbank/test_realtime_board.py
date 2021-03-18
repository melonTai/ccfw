import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from ccfw.bitbank.realtime_stream import RealTimeBoard
import asyncio
import traceback

class Test(RealTimeBoard):
    async def watch(self):
        while True:
            print("hi")
            if self.board:
                print(self.board['asks'][0]['price'], self.board['asks'][0]['size'])
                print(self.board['bids'][0]['price'], self.board['bids'][0]['size'])
            await asyncio.sleep(1)
    async def run(self):
        while True:
            try:
                await asyncio.gather(
                    self.watch(),
                    self.wait()
                    )
            except Exception as e:
                print(traceback.format_exc())

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    import logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.DEBUG)
    test = Test(
        symbol = 'xrp_jpy',
    )
    # test.logger.setLevel(logging.DEBUG)
    # sh = logging.StreamHandler()
    # sh.setFormatter(formatter)
    # sh.setLevel(logging.DEBUG)
    # test.logger.addHandler(sh)
    asyncio.run(test.run())
    exit()
