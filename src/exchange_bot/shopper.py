from dca.order import Order
from exchange_bot.trade import Trade

class Shopper:
    def __init__(self):
        self.name = ""
        self.client = None
        self.__placed_trades = dict() # Dictionary of 1 order to N trades

    '''
    Virtual Protected Methods overridden by exchanges shopper/mock shopper
    '''

    '''
    Get the last price action of the pair
        _get_price('ETHUSDT') -> 1232.435
    '''
    def _get_price(self, asset: str, currency: str) -> float:
        raise Exception("This method is a virtual method for base class.")

    '''
    Get the minimum quote quantity for symbol 
        i.e. for ETHUSD pair, minimum quantity to buy might be 0.01 ETH
        _get_minimum_quote_quantity_for_symbol('ETHUSDT') -> 0.0113124
    '''
    def _get_minimum_quote_quantity_for_symbol(self, asset: str, currency: str) -> float:
        raise Exception("This method is a virtual method for base class.")

    '''
    Get the available amount on the user's account for the asset
        _get_available_amount('USDT') -> 13942.24
    '''
    def _get_available_amount(self, asset: str) -> float:
        raise Exception("This method is a virtual method for base class.")

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
    def get_placed_trades(self):
        return self.__placed_trades

    '''
    Takes a Order from the JSON file and places the order. Returns the Traded Order.
    '''
    def order(self, order: Order) -> Trade:
        raise Exception("This method is a virtual method for base class.")

    
    def calculate_pnl_for_order(self, order_id: int):
        trades = self.__placed_trades[order_id]

        order_pnl = 0.0
        order_current_value = 0.0

        for trade in trades:
            trade_value_usd = self._get_price(trade['asset'], 'USDT') * trade['amount_of_asset_bought']
            pnl_usd = trade_value_usd - trade['quantity_of_usd_used']

            trade.last_pnl = pnl_usd
            trade.last_delta_percentage = trade_value_usd / trade['quantity_of_usd_used'] * 100

            order_current_value += trade_value_usd
            order_pnl += pnl_usd
        
        return order_pnl

    
    def calculate_total_pnl(self):
        total_pnl = 0.0

        for order_id, _ in self.__placed_trades.items():
            total_pnl += calculate_pnl_for_order(order_id)

        return total_pnl