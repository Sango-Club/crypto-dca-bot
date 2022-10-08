import pycron
from typing import Dict
import os
from multiprocessing import Process, Lock
import time
import sys
import coloredlogs, logging

from .order import Order
from .alerter import Alerter
from .shopper import Shopper
class DCABot:
    def __init__(self, dca_config: Dict):
        self.logger = logging.getLogger("dca_bot")
        coloredlogs.install(logger=self.logger)
        
        self.__dca_config = dca_config
        self.__processes = []
        self.__running = False
        
        self.orders = []
        for order in dca_config["orders"]:
            self.orders.append(Order(order))

        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        telegram_token = os.getenv("TELEGRAM_TOKEN")

        twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        twitter_consummer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        gmail_oauth = os.getenv("GMAIL_OAUTH_JSON")
        gmail_receiver = os.getenv("GMAIL_RECEIVER_ADDRESS")
        gmail_sender = os.getenv("GMAIL_SENDER_ADDRESS")

        discord_token = os.getenv("DISCORD_TOKEN")
        discord_updates_webhook = os.getenv("DISCORD_UPDATES_WEBHOOK")

        self.alerter = Alerter(dca_config["notifications"],
                        gmail_receiver, gmail_sender, gmail_oauth, 
                        telegram_token, telegram_chat_id, twitter_consumer_key, 
                        twitter_consummer_secret, twitter_access_token, 
                        twitter_access_token_secret,
                        discord_token, discord_updates_webhook)
        
        self.shopper = Shopper(self.orders)

        self.collection = {
            "orders": []
        }
        

    def __del__(self):
        self.__running = False
        for p in self.__processes:
            p.join()

        self.alerter.notify("DCA Bot has stopped!")     

    def run(self):
        mutex = Lock()
        self.__running = True
        self.alerter.notify("DCA Bot has started!")
        for order in self.orders:
            self.__processes.append(Process(target=self.__run_job_process, args=(order, mutex)))
            self.__processes[-1].start()

    def __run_job_process(self, order: Order, mutex: Lock):
        while self.__running:
            if pycron.is_now(order.cron):
                mutex.acquire()

                try:
                    msg = (f"------------------\n"
                            f"**Order Requested**: \n"
                            f"Exchange : {order.exchange} \n"
                            f"Asset : {order.asset} \n"
                            f"Quantity : {order.quantity} {order.currency} \n"
                    f"------------------\n")
                    self.logger.info(msg)
                    trade = self.shopper.order(order)
                    self.collection["orders"].append(
                        {
                            "asset": trade.asset,
                            "currency": trade.currency,
                            "amount_of_asset_bought": trade.amount_of_asset_bought,
                            "price_per_unit": trade.price_per_unit,
                            "quantity_of_currency_used": trade.quantity_of_currency_used,
                            "exchange": trade.exchange
                        }
                    )
                    
                    # TO DO
                    # Order doesn't mean you filled exactly what you ask
                    # V1: Assume Order is exactly what was filled
                    # V2: Order should return an order id. Use that order ID to check order filled.
                    # Store price of filled orders for PNL
                    # Store every trade in a collection with N Asset bought for X Quantity
                    # To calculate a trade's PNL, get current price of asset in currency, simple calculation
                    # Iterate over all trades to get PNL of each trades and get total PNL


                    self.alerter.notify(msg)
                    
                except Exception as e:
                    self.logger.error(str(e))
                    self.alerter.notify(str(e))

                mutex.release()
                time.sleep(60)
            else:
                time.sleep(20)
