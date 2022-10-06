import binance
from src.dca.order import Order
from src.utils.exceptions import BadDCAOrderException

class BinanceShopper:
    def __init__(self, api_key, api_secret):
        self.client = binance.Client(api_key, api_secret)
    
    def get_minimum_quote_quantity_for_symbol(self, symbol):
        symbolInfo = self.client.get_symbol_info(symbol=symbol)

        for elem in symbolInfo["filters"]:
            if elem["filterType"] == "MIN_NOTIONAL":
                return elem["minNotional"]
        
        return "inf"

    def _get_asset_available_amount(self, asset: str):
        asset_info = self.client.get_asset_balance(asset=asset, recvWindow=50000)
        return asset_info["free"]

    def _get_price(self, symbol: str) -> str:
        symbol_stats = self.client.get_symbol_ticker(symbol=symbol)
        return symbol_stats["price"]

    def order(self, order: Order):
        symbol = f"{order.asset}{order.currency}"
        min_quote_quantity = self.get_minimum_quote_quantity_for_symbol(symbol)
        
        if float(min_quote_quantity) > order.quantity:
            raise BadDCAOrderException(f"Tried to buy {order.quantity}{order.currency} of {order.asset}, but minimum quote quantity is {min_quote_quantity}.")

        currency_available = self._get_asset_available_amount(order.currency)

        if float(currency_available) <= order.quantity:
            raise BadDCAOrderException(f"Tried to buy {order.quantity}{order.currency} of {order.asset}, but only {currency_available}{order.currency} is available on account.")
        
        order = self.client.order_market_buy(symbol=symbol, quoteOrderQty=order.quantity, recvWindow=50000)
        return order

