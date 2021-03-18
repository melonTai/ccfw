from ...base.socketio_template import SocketIOClient
class RealTimeBase(SocketIOClient):
    endpoint = 'wss://stream.bitbank.cc'
    def __init__(self,symbol,**kargs):
        self.symbol = symbol
        super().__init__(endpoint = self.endpoint, **kargs)
