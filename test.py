from src.shops.binance import BinanceShopper
from src.common.order import Order

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    shopper = BinanceShopper(os.getenv("BINANCE_KEY"), os.getenv("BINANCE_SECRET"))
    order_dict = {
        "asset": "ETH",
        "currency": "BUSD",
        "quantity": 24.0,
        "frequency": "* * * * *",
        "exchange": "binance"
    }
    shopper.order(Order(order_dict))