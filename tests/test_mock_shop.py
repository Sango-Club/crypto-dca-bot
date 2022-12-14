import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.shops.mock import MockShop
from src.utils.exceptions import BadDCAOrderException, NotYetImplemented, UnimplementedAndNotPlanned
from src.shops.shop import Shop
from src.common.trade import Trade
from src.common.order import Order

order1 = {
    "asset": "ETH",
    "currency": "USDT",
    "quantity": 110.9,
    "frequency": "* 2 7 * *", 
    "exchange": "mock" 
}
order2 = {
    "asset": "BTC",
    "currency": "USDT",
    "quantity": 10.8,
    "frequency": "* * * * *",
    "exchange": "mock"
}
order3 = {
    "asset": "BNB",
    "currency": "USDT",
    "quantity": 0.00064,
    "frequency": "* 5 * * SUN",
    "exchange": "mock"
}
order4 = {
    "asset": "BNB",
    "currency": "USDT",
    "quantity": 2000000000.0,
    "frequency": "* 5 * * SUN",
    "exchange": "mock"
}
order5 = {
    "asset": "BNB",
    "currency": "BUST",
    "quantity": 0.00064,
    "frequency": "* 5 * * SUN",
    "exchange": "mock"
}

