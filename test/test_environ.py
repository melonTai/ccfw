import math
from decimal import getcontext, Decimal

def round_down(x, n = 4):
    getcontext().prec = n
    x = Decimal(x)
    return float(x)

print(-4 % 3)