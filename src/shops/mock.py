from dca.order import Order
from shops.shop import Shop
from shops.trade import Trade

class MockShop(Shop):
    def __init__(self):

        # Dictionary of set prices for predefined pairs, as well as their callable increments
        # Immutable outside the class
        self.__prices = {
            "ETH/USDT": (1000.0, 100.0),
            "BTC/USDT": (10000.0, 1000.0),
            "BNB/USDT": (100.0, 10.0)
        }

        self.__available_usdt = 1e6

    ## TO DO: what if pair isn't supported by mock

    '''
    Overriden virtual methods
    '''

    '''
    Get the last price action of the pair
        _get_price('ETHUSDT') -> 1232.435
    '''
    def _get_price(self, asset: str, currency: str) -> float:
        return self.__prices[self.__asset_to_pair(asset, currency)][0]

    '''
    Get the minimum quote quantity for symbol 
        i.e. for ETHUSD pair, minimum quantity to buy might be 0.01 ETH
        _get_minimum_quote_quantity_for_symbol('ETH', 'USDT') -> 0.0113124
    '''
    def _get_minimum_quote_quantity_for_symbol(self, asset: str, currency: str) -> float:
        if asset == "ETH":
            return 0.001
        elif asset == "BTC":
            return 0.00001
        elif asset == "BNB":
            return 0.01
        else:
            raise Exception("Asset not supported by Mock Shop")

    '''
    Get the maximum quote quantity for symbol 
        i.e. for ETHUSD pair, minimum quantity to buy might be 0.01 ETH
        _get_maximum_quote_quantity_for_symbol('ETHUSDT') -> 199.0113124
    '''
    def _get_maximum_quote_quantity_for_symbol(self, asset: str, currency: str) -> float:
        if asset == "ETH":
            return 100.0
        elif asset == "BTC":
            return 10.0
        elif asset == "BNB":
            return 1000.0
        else:
            raise Exception("Asset not supported by Mock Shop")

    '''
    Get the available amount on the user's account for the asset
        _get_available_amount('USDT') -> 13942.24
    '''
    def _get_available_amount(self, asset: str) -> float:
        return float("inf") # should be dependent on waht you spent

    '''
    Public Methods
    '''

    '''
    Pump asset with fixed increment
    '''
    def pump_asset(self, asset: str, currency: str):
        pair = self.__asset_to_pair(asset, currency)
        self.__prices[pair][0] += self.__prices[pair][1]

    '''
    Dump asset with fixed increment
    '''
    def dump_asset(self, asset: str, currency: str):
        pair = self.__asset_to_pair(asset, currency)
        new_price = self.__prices[pair][0] - self.__prices[pair][1]
        if new_price < 0.0:
            self.__prices[pair][0] = 0.0
        else:
            self.__prices[pair][0] = new_price

    '''
    Takes a Order from the JSON file and places the order. Returns the Traded Order.
    '''
    def order(self, order: Order) -> Trade:
        price = self._get_price(order.asset, order.currency)
        price = self.get_price(order.asset, order.currency)
        price_in_usd = self.get_price(order.currency, "USD")
        available_amount = self._get_available_amount(order.currency)
        min_quote_quantity = self.get_minimum_quote_quantity_for_symbol(symbol)
        max_quote_quantity = self.get_maximum_quote_quantity_for_symbol(symbol)

        print(min_quote_quantity)
        print(max_quote_quantity)
        qty_of_asset_to_buy = float(order.quantity)/price

        if float(min_quote_quantity) > qty_of_asset_to_buy:
            raise BadDCAOrderException(f"Tried to buy {order.asset} {qty_of_asset_to_buy} for {order.quantity} {order.currency}, but minimum quote quantity is {min_quote_quantity}.")

        if float(max_quote_quantity) < qty_of_asset_to_buy:
            raise BadDCAOrderException(f"Tried to buy {order.asset} {qty_of_asset_to_buy} for {order.quantity} {order.currency}, but maximum quote quantity is {max_quote_quantity}.")

        if float(available_amount) <= order.quantity:
            raise BadDCAOrderException(f"Tried to buy {order.asset} {qty_of_asset_to_buy} for {order.quantity} {order.currency}, but only {available_amount} {order.currency} is available on account.")

        print(f"Requesting to buy {qty_of_asset_to_buy} {order.asset} at {price} {order.currency} per {order.asset} for {order.quantity} {order.currency}")



    '''
    Private Methods
    '''
    
    def __asset_to_pair(self, asset: str, currency: str) -> str:
        return f'{asset}/{currency}'