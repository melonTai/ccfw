import requests
import json

_endPoint = 'https://api.coin.z.com/public'

def get_ticker(symbol):
    path     = '/v1/ticker?symbol={symbol}'.format(symbol = symbol)
    response = requests.get(_endPoint + path)
    return response.json()['data'][0]

def get_board(symbol):
    path     = '/v1/orderbooks?symbol={symbol}'.format(symbol = symbol)
    response = requests.get(_endPoint + path)
    return response.json()['data']
if __name__ == '__main__':
    res = get_ticker('XRP_JPY')
    print(type(res))
    print(res)
