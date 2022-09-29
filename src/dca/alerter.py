from telegram.telegram_bot import TelegramBot
from twitter.twitter_bot import TwitterBot
from gmail.gmail_bot import GmailBot

class Alerter:
    def __init__(self, notification_dict, 
                 gmail_receiver, gmail_sender, gmail_oauth, 
                 telegram_token, telegram_chat_id,
                 twitter_consumer_key, twitter_consummer_secret, 
                 twitter_access_token, twitter_access_token_secret):

        self.twitter = notification_dict["twitter"]
        self.telegram = notification_dict["telegram"]
        self.gmail = notification_dict["gmail"]

        if self.gmail:
            self.__gmail_bot = GmailBot(gmail_sender, gmail_receiver, f"../{gmail_oauth}")
        
        if self.telegram:
            self.__telegram_bot = TelegramBot(telegram_token, telegram_chat_id)
        
        if self.twitter:
            self.__twitter_bot = TwitterBot(twitter_consumer_key, twitter_consummer_secret,
                                        twitter_access_token, twitter_access_token_secret)
    
    def notify(self, msg):
        if self.gmail:
            self.__gmail_bot.send_mail(msg)
            
        if self.telegram:
            self.__telegram_bot.echo_message(msg)
            
        if self.twitter:
            self.__twitter_bot.tweet()
        
        