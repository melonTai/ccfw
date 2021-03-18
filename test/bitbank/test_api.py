import python_bitbankcc
import login
from pprint import pprint

prv = python_bitbankcc.private(login.API_KEY, login.API_SECRET)

pprint(prv.get_asset())

value = prv.order(
    'xrp_jpy', # ペア
    '1', # 価格
    '1', # 注文枚数
    'buy', # 注文サイド
    'limit' # 注文タイプ
)
print(value)
"""
{'order_id': 13117487312, 'pair': 'xrp_jpy', 'side': 'buy', 'type': 'limit', 'start_amount': '1.0000', 'remaining_amount': '1.0000', 'executed_amount': '0.0000', 'price': '1.000', 'average_price': '0.000', 'ordered_at': 1615912027287, 'status': 'UNFILLED'}
"""