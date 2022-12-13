from dca.order import Order, OrderStats
from shops.trade import Trade
from time import time
from typing import List

'''
Base class for all Shops (Binance, KuCoin, Nexo, Mock...)
    -> Base methods to override
    -> Public methods available regardless of shop specificity by using overriden methods (PNL related)
'''
class Shop:
    def __init__(self):
        self.name = ""
        self.client = None
        self.__placed_trades = dict() # Dictionary of 1 order to N trades
        self.__order_stats = dict()

    '''
    Virtual Protected Methods overridden by exchanges shopper/mock shopper
    '''

    '''
    Get the last price action of the pair
        _get_price('ETHUSDT') -> 1232.435
    '''
    def _get_price(self, asset: str, currency: str) -> float:
        raise Exception("This method is a virtual method for base class, please override.")

    '''
    Get the minimum quote quantity for symbol 
        i.e. for ETHUSD pair, minimum quantity to buy might be 0.01 ETH
        _get_minimum_quote_quantity_for_symbol('ETHUSDT') -> 0.0113124
    '''
    def _get_minimum_quote_quantity_for_symbol(self, asset: str, currency: str) -> float:
        raise Exception("This method is a virtual method for base class, please override.")

    '''
    Get the maximum quote quantity for symbol 
        i.e. for ETHUSD pair, minimum quantity to buy might be 0.01 ETH
        _get_maximum_quote_quantity_for_symbol('ETHUSDT') -> 199.0113124
    '''
    def _get_maximum_quote_quantity_for_symbol(self, asset: str, currency: str) -> float:
        raise Exception("This method is a virtual method for base class, please override.")

    '''
    Get the available amount on the user's account for the asset
        _get_available_amount('USDT') -> 13942.24
    '''
    def _get_available_amount(self, asset: str) -> float:
        raise Exception("This method is a virtual method for base class, please override.")

    '''
    Add a trade to an order. A DCA Order has N Trades associated to it
    '''
    def _add_trade_to_order(self, order_id: int, trade: Trade):
        if not order_id in self.__placed_trades:
            self.__placed_trades[order_id] = []

        self.__placed_trades[order_id].append(trade)

    '''
    Public Methods
    '''

    '''
    Gets the map of all orders and associated trades
    '''
    @property
    def get_placed_trades(self) -> List[Trade]:
        return self.__placed_trades

    '''
    Get all trades for a specific order
    '''
    @property
    def get_order_trades(self, order_id: int) -> Trade:
        return self.__placed_trades[order_id]

    @property
    def get_order_stats(self) -> List[OrderStats]:
        return self.__order_stats

    '''
    Takes a Order from the JSON file and places the order. Returns the Traded Order.
    '''
    def order(self, order: Order) -> Trade:
        raise Exception("This method is a virtual method for base class, please override.")
    
    '''
    Calculate the PNL of N trades in 1 order
    '''
    def calculate_order_pnl(self, order_id: int) -> float:
        trades = self.__placed_trades[order_id]

        order_pnl = 0.0

        for trade in trades:
            trade_value_usd = self._get_price(trade['asset'], 'USDT') * trade['amount_of_asset_bought']
            pnl_usd = trade_value_usd - trade['quantity_of_usd_used']

            trade.last_pnl = pnl_usd
            trade.last_delta_percentage = trade_value_usd / trade['quantity_of_usd_used'] * 100
            trade.last_update_timestamp = time()

            order_pnl += pnl_usd
        
        return order_pnl

    
    '''
    Calculate the total PNL across all orders
    '''
    def calculate_total_pnl(self) -> float:
        total_pnl = 0.0

        for order_id, _ in self.__placed_trades.items():
            total_pnl += self.calculate_pnl_for_order(order_id)

        return total_pnl

    
    '''
    Calculate Order Statistics
    '''
    def get_order_statistics(self, order_id: int) -> OrderStats:
        self.calculate_order_pnl(order_id)
        trades = self.__placed_trades[order_id]
        stats = OrderStats(order_id)

        for trade in trades:
            stats.current_value += trade.quantity_of_usd_used + trade.pnl
            stats.total_spent += trade.quantity_of_usd_used
        
        stats.delta_percentage = ((stats.current_value / stats.total_spent) - 1) * 100
        stats.timestamp = time()

        return stats
