import pycron
from typing import Dict
import os
from multiprocessing import Process, Lock
import time
import sys

from telegram.telegram_bot import TelegramBot
from twitter.twitter_bot import TwitterBot
from gmail.gmail_bot import GmailBot
class DCABot:
    def __init__(self, dca_config: Dict):
        self.__dca_config = dca_config
        self.__processes = []
        self.__running = False

        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        telegram_token = os.getenv("TELEGRAM_TOKEN")

        twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        twitter_consummer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        gmail_oauth = os.getenv("GMAIL_OAUTH_JSON")
        self.__gmail_receiver = os.getenv("GMAIL_RECEIVER_ADDRESS")
        gmail_sender = os.getenv("GMAIL_SENDER_ADDRESS")

        self.__gmail_bot = GmailBot(gmail_sender, gmail_oauth)
        self.__telegram_bot = TelegramBot(telegram_token, telegram_chat_id)
        self.__twitter_bot = TwitterBot(twitter_consumer_key, twitter_consummer_secret,
                                        twitter_access_token, twitter_access_token_secret)

        if not self.__twitter_bot.verify_credentials():
            self.__telegram_bot.echo_message("Twitter Bot failed to authenticate!")     
            self.__gmail_bot.send_mail(to=self.__gmail_receiver, 
                                   subject="Twitter Bot Info", 
                                   contents="Twitter Bot failed to authenticate!")                         
        
        # Telegram Hello
        if not self.__telegram_bot.echo_message("DCA Bot is Running!"):
            sys.exit("The Telegram Bot failed to send a message. It MUST be running for the app to stay alive. Exiting...")

        # Twitter Hello
        if not self.__twitter_bot.tweet("DCA Bot is Running!"):
            self.__telegram_bot.echo_message("Twitter Bot failed to tweet!")     

        # Gmail Hello
        if not self.__gmail_bot.send_mail(to=self.__gmail_receiver, 
                                   subject="DCA Bot Start!", 
                                   contents="DCA Bot is Running"):
            self.__telegram_bot.echo_message("Gmail Bot failed to send email!")     
    
    def __del__(self):
        self.__running = False
        for p in self.__processes:
            p.join()

    def run(self):
        mutex = Lock()
        self.__running = True
        for order in self.__dca_config["orders"]:
            self.__processes.append(Process(target=self.__run_job_process, args=(order, mutex)))
            self.__processes[-1].start()

    def __run_job_process(self, order, mutex):
        while self.__running:
            if pycron.is_now(order["frequency"]):
                mutex.acquire()
                msg = '''f"Order Filled: \n"
                    f"Exchange : {order['exchange']} \n"
                    f"Pair : {order['pair']} \n"
                    f"Quantity : {order['quantity']} \n"'''
                if not self.__telegram_bot.echo_message(msg):
                    sys.exit("The Telegram Bot failed to send a message. It MUST be running for the app to stay alive. Exiting...")
                
                if not self.__twitter_bot.tweet(msg):
                    self.__telegram_bot.echo_message("Twitter Bot failed to tweet!")

                if not self.__gmail_bot.send_mail(to=self.__gmail_receiver, 
                                           subject="DCA Order Update", 
                                           contents=msg):
                    self.__telegram_bot.echo_message("Gmail Bot failed to send email!")     
                mutex.release()
                time.sleep(60)
            else:
                time.sleep(20)
