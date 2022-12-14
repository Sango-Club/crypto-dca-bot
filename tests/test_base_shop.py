import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.exceptions import BadDCAOrderException, NotYetImplemented, UnimplementedAndNotPlanned
from src.shops.shop import Shop
from src.shops.trade import Trade
from src.common.order import Order

import pytest

order = {
    "asset": "ETH",
    "currency": "USDT",
    "quantity": 110.9,
    "frequency": "* 2 7 * *", 
    "exchange": "mock" 
}

def test_constructor():
    order_obj = Order(order)
    order_obj.set_order_id(1)

    shop = Shop()

    assert(shop.get_order_stats() == {})
    
    with (pytest.raises(BadDCAOrderException)):
        assert(shop.get_order_trades(1) == [])
    assert(shop.get_placed_trades() == {})

    with (pytest.raises(BadDCAOrderException)):
        assert(shop.calculate_order_pnl(2.0) == 0.0)
