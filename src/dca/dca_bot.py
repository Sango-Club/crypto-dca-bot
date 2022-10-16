import pycron
from typing import Dict
import os
from multiprocessing import Process, Lock
import time
import sys
import coloredlogs, logging

from .order import Order
from .order_stats import OrderStats
from .alerter import Alerter
from .shopper import Shopper
class DCABot:
    def __init__(self, dca_config: Dict):
        self.logger = logging.getLogger("dca_bot")
        coloredlogs.install(logger=self.logger)
        
        self.__dca_config = dca_config
        self.__orders_processes = []
        self.__orders_running = False
        self.__pnl_process = None
        self.__pnl_running = False
        
        self.collection = {
            "stats": OrderStats(),
            "trades": {}
        }

        self.orders = {}
        order_id = 1

        for order in dca_config["orders"]:
            self.orders[order_id] = Order(order)
            self.collection["trades"][order_id] = []
            self.orders[order_id].set_order_id(order_id)
            order_id += 1
        
        self._pnl_frequency_updates = dca_config["notifications"]["pnl_frequency_updates"]

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
        

    def __del__(self):
        self.__orders_running = False
        self.__pnl_running = False
        for p in self.__orders_processes:
            p.join()
        
        self.__pnl_process.join()
        
        self.alerter.notify("DCA Bot has stopped!")

    def run(self):
        mutex = Lock()
        self.__orders_running = True
        self.alerter.notify("DCA Bot has started!")
        for order in self.orders:
            self.__orders_processes.append(Process(target=self.__run_order_process, args=(order, mutex)))
            self.__orders_processes[-1].start()
        
        self.__pnl_process = Process(target=self.__run_pnl_process, args=(mutex))
        self.__pnl_process.start()
    
    
    def __run_pnl_process(self, mutex: Lock):
        while self.__pnl_running:
            if pycron.is_now(self._pnl_frequency_updates):
                mutex.acquire()
                
                current_value = 0.0
                total_pnl = 0.0

                for order_id in self.collection["trades"]:

                    order_current_value = 0.0
                    order_pnl = 0.0

                    for trade in self.collection["trades"][order_id]:
                        try:
                            trade_value_usd = self.shopper.get_price(trade['asset'], 'USD', trade['exchange']) * trade['amount_of_asset_bought']
                            pnl_usd = trade_value_usd - trade['quantity_of_usd_used']
                            order_current_value += trade_value_usd
                            order_pnl += pnl_usd
                        
                        except Exception as e:
                            self.logger.error(e)
                            self.alerter.notify(e)
                    
                    self.orders[order_id].stats.current_value = order_current_value
                    self.orders[order_id].stats.pnl = order_pnl

                    current_value += order_current_value
                    total_pnl += total_pnl

                    self.orders[order_id].stats.delta = (1 - self.orders[order_id].total_spent / order_current_value) * 100
                    
                    msg = (
                                f"------------------\n"
                                f"*** Profit and Losses ***\n"
                                f"- Order {order_id} of [{trade['asset']}] for [{trade['quantity_of_currency_used']} {trade['currency']}]\n"
                                f"- Current Value: {order_current_value} USD\n"
                                f"- PNL: {order_pnl:.4f} USD\n"
                                f"- Performance: {self.orders[order_id].stats.delta}%\n"
                                f"------------------\n"
                    )

                    self.orders[order_id].stats.timestamp = int(time.time() * 1000)

                    self.logger.info(msg)
                    self.alerter.notify(msg)
                

                self.collection["stats"].current_value = current_value
                self.collection["stats"].pnl = total_pnl
                self.collection["stats"].delta = (1 - self.collection["stats"].total_spent / self.collection["stats"].current_value) * 100
                self.collection["stats"].timestamp = int(time.time() * 1000)

                msg = (
                    f"------------------\n"
                    f"*** Total Profit and Losses ***\n"
                    f"- Current Value: {current_value} USD\n"
                    f"- PNL: {total_pnl:.4f} USD\n"
                    f"- Performance: {self.collection['stats'].delta}%\n"
                    f"------------------\n"
                )

                self.logger.info(msg)
                self.alerter.notify(msg)

                mutex.release()
                time.sleep(60)
            else:
                time.sleep(20)

    def __run_order_process(self, order: Order, mutex: Lock):
        while self.__orders_running:
            if pycron.is_now(order.cron):
                mutex.acquire()

                try:
                    msg = (
                        f"------------------\n"
                        f"*** Order Requested ***: \n"
                        f"Exchange : {order.exchange} \n"
                        f"Asset : {order.asset} \n"
                        f"Quantity : {order.quantity} {order.currency} \n"
                        f"------------------\n"
                    )
                    self.logger.info(msg)
                    trade = self.shopper.order(order)
                    self.orders[order.order_id].stats.total_spent += trade.quantity_of_usd_used
                    self.collection["stats"].total_spent += trade.quantity_of_usd_used
                    
                    self.collection["trades"][order.order_id].append({
                            "asset": trade.asset,
                            "currency": trade.currency,
                            "amount_of_asset_bought": trade.amount_of_asset_bought,
                            "price_per_unit": trade.price_per_unit,
                            "quantity_of_currency_used": trade.quantity_of_currency_used,
                            "quantity_of_usd_used": trade.quantity_of_usd_used,
                            "exchange": trade.exchange,
                    })
                    
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
