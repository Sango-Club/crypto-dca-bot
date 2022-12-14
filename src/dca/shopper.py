from exchange_bot.binance import BinanceShopper
from exchange_bot.nexo import NexoShopper
from utils.exceptions import NotYetImplemented, UnimplementedAndNotPlanned
from dca.order import Order
from typing import List
import os
import time

class Shopper:
    def __init__(self, orders: List[Order]):
        self.shoppers = {}
        time.sleep(5)

        for elem in orders:
            if elem.exchange == "binance":
                self.shoppers["binance"] = BinanceShopper(os.getenv("BINANCE_KEY"), os.getenv("BINANCE_SECRET"))
            elif elem.exchange == "nexo":
                self.shoppers["nexo"] = NexoShopper(os.getenv("NEXO_PUBLIC_KEY"), os.getenv("NEXO_SECRET_KEY"))
            elif elem.exchange == "ftx":
                raise NotYetImplemented("FTX Exchange is not yet implemented")
            elif elem.exchange == "kucoin":
                raise NotYetImplemented("KuCoin Exchange is not yet implemented")
            else:
                raise UnimplementedAndNotPlanned(f"Exchange [{elem.exchange}] is not implemented.")
        
    def order(self, order: Order):
        if order.exchange in self.shoppers:
            self.shoppers[order.exchange].order(order)
        else:
            raise NotYetImplemented(f"Exchange [{order.exchange}] is not implemented.")