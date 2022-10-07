import nexo
from dca.order import Order
from utils.exceptions import BadDCAOrderException

class NexoShopper:
    def __init__(self, api_key, api_secret):
        self.client = nexo.Client(api_key, api_secret)

    def _get_price(self, symbol: str) -> float:
        symbol_stats = self.client.get_price_quote(symbol, 1.0, "buy")
        return float(symbol_stats["price"])
    
    def get_minimum_quote_quantity_for_symbol(self, symbol):
        pairs_info = self.client.get_pairs()
        return float(pairs_info["min_limits"][symbol])
    
    def get_maximum_quote_quantity_for_symbol(self, symbol):
        pairs_info = self.client.get_pairs()
        return float(pairs_info["max_limits"][symbol])

    def _get_available_amount(self, asset: str) -> float:
        balances = self.client.get_account_balances()

        for wb in balances["balances"]:
            if wb["assetName"] == asset:
                return float(wb["availableBalance"])
        
        return 0.0

    def order(self, order: Order):
        symbol = f"{order.asset}/{order.currency}"
        price = self._get_price(symbol)
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

        order = self.client.place_order(symbol, "buy", "market", qty_of_asset_to_buy)
        return order

