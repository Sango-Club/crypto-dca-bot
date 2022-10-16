import binance
from dca.order import Order
from exchange_bot.trade import Trade
from utils.exceptions import BadDCAOrderException

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

    def get_price(self, asset: str, currency: str) -> str:
        symbol = f"{asset}{currency}"
        symbol_stats = self.client.get_symbol_ticker(symbol=symbol)
        return symbol_stats["price"]

    def order(self, order: Order) -> Trade:
        symbol = f"{order.asset}{order.currency}"
        min_quote_quantity = self.get_minimum_quote_quantity_for_symbol(symbol)
        
        if float(min_quote_quantity) > float(order.quantity):
            raise BadDCAOrderException(f"Tried to buy {order.quantity}{order.currency} of {order.asset}, but minimum quote quantity is {min_quote_quantity}.")

        currency_available = self._get_asset_available_amount(order.currency)

        if float(currency_available) <= float(order.quantity):
            raise BadDCAOrderException(f"Tried to buy {order.quantity}{order.currency} of {order.asset}, but only {currency_available}{order.currency} is available on account.")
        
        order = self.client.order_market_buy(symbol=symbol, quoteOrderQty=order.quantity, recvWindow=50000)
    
        price_per_unit = self.get_price(order.asset, order.currency)
        amount_of_asset_bought = order.quantity/price_per_unit
        price_in_usd = self.get_price(order.currency, "USD")
        trade = Trade(order.asset, order.currency, price_per_unit, amount_of_asset_bought, order.quantity, order.quantity*price_in_usd, order.exchange)

        return trade

