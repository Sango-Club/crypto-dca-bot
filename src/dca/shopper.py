from src.exchange_bot.binance import BinanceShopper
from src.utils.exceptions import NotYetImplemented, UnimplementedAndNotPlanned
from src.dca.order import Order
from typing import List
import os

class Shopper:
    def __init__(self, orders: List[Order]):
        self.shoppers = {}

        for elem in orders:
            if elem["exchange"] == "binance":
                self.shoppers["binance"] = BinanceShopper(os.getenv("BINANCE_KEY"), os.getenv("BINANCE_SECRET"))
            if elem["exchange"] == "nexo":
                raise NotYetImplemented("Nexo Exchange is not yet implemented")
            if elem["exchange"] == "ftx":
                raise NotYetImplemented("FTX Exchange is not yet implemented")
            if elem["exchange"] == "kucoin":
                raise NotYetImplemented("KuCoin Exchange is not yet implemented")
            else:
                raise UnimplementedAndNotPlanned(f"Exchange [{elem}] is not implemented.")
        
    def order(self, order: Order):
        if order.exchange in self.shoppers:
            return self.shoppers[order.exchange].order(order)
        else:
            raise NotYetImplemented(f"Exchange [{order.exchange}] is not implemented.")