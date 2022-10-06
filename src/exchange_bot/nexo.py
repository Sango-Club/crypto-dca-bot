import nexo
from dca.order import Order
from utils.exceptions import BadDCAOrderException

class NexoShopper:
    def __init__(self, api_key, api_secret):
        self.client = nexo.Client(api_key, api_secret)

    def _get_price(self, symbol: str) -> float:
        symbol_stats = self.client.get_price_quote(symbol, 1.0, "buy")
        return float(symbol_stats["price"])

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

        if float(available_amount) <= order.quantity:
            raise BadDCAOrderException(f"Tried to buy {order.quantity}{order.currency} of {order.asset}, but only {available_amount}{order.currency} is available on account.")
        
        qty_of_asset_to_buy = float(order.quantity)/price

        print(f"Requesting to buy {qty_of_asset_to_buy}{order.currency} of {order.asset} at {price}{order.currency} per {order.asset}")

        order = self.client.place_order(symbol, "buy", "market", qty_of_asset_to_buy)
        return order

