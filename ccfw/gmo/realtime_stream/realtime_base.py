from ...base.websocket_template import WebsocketClient
class RealTimeBase(WebsocketClient):
    endpoint = 'wss://api.coin.z.com/ws/public/v1'
    def __init__(self, symbol,**kargs):
        self.symbol = symbol
        super().__init__(endpoint = self.endpoint, **kargs)
