import pycron
from typing import Dict
import os
from multiprocessing import Process, Lock
import time

from telegram.telegram_bot import TelegramBot

class DCABot:
    def __init__(self, dca_config: Dict):
        self.__dca_config = dca_config

        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        telegram_token = os.getenv("TELEGRAM_TOKEN")
        
        self.__telegram_bot = TelegramBot(telegram_token, telegram_chat_id)
        self.__telegram_bot.echo_message("DCA Bot is Running!")

        self.__processes = []
        self.__running = True
    
    def __del__(self):
        self.__running = False
        for p in self.__processes:
            p.join()

    def run(self):
        mutex = Lock()
        for order in self.__dca_config["orders"]:
            self.__processes.append(Process(target=self.__run_job_process, args=(order, mutex)))
            self.__processes[-1].start()

    def __run_job_process(self, order, mutex):
        while self.__running:
            if pycron.is_now(order["frequency"]):
                mutex.acquire()
                self.__telegram_bot.echo_message(f"Order Filled: \n"
                                               f"Exchange : {order['exchange']} \n"
                                               f"Pair : {order['pair']} \n"
                                               f"Quantity : {order['quantity']} \n")
                mutex.release()
                time.sleep(60)
            else:
                time.sleep(20)
