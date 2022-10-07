from telegram_bot.telegram_bot import TelegramBot
from twitter_bot.twitter_bot import TwitterBot
from gmail_bot.gmail_bot import GmailBot
from discord_bot.discord_bot import DiscordBot

class Alerter:
    def __init__(self, notification_dict, 
                 gmail_receiver, gmail_sender, gmail_oauth, 
                 telegram_token, telegram_chat_id,
                 twitter_consumer_key, twitter_consummer_secret, 
                 twitter_access_token, twitter_access_token_secret,
                 discord_token, discord_updates_webhook):

        if "twitter" in notification_dict:
            self.twitter = notification_dict["twitter"]
        else:
            self.twitter = False
        
        if "telegram" in notification_dict:
            self.telegram = notification_dict["telegram"]
        else:
            self.telegram = False

        if "gmail" in notification_dict:
            self.gmail = notification_dict["gmail"]
        else:
            self.gmail = False
        
        if "discord" in notification_dict:
            self.discord = notification_dict["discord"]
        else:
            self.discord = False

        if self.gmail:
            self.__gmail_bot = GmailBot(gmail_sender, gmail_receiver, f"../{gmail_oauth}")
        
        if self.telegram:
            self.__telegram_bot = TelegramBot(telegram_token, telegram_chat_id)
        
        if self.twitter:
            self.__twitter_bot = TwitterBot(twitter_consumer_key, twitter_consummer_secret,
                                        twitter_access_token, twitter_access_token_secret)

        if self.discord:
            self.__discord_bot = DiscordBot(discord_token, discord_updates_webhook)
            self.__discord_bot.run_bot()
    
    def notify(self, msg):
        if self.gmail:
            self.__gmail_bot.send_mail(msg)

        if self.telegram:
            self.__telegram_bot.echo_message(msg)
            
        if self.twitter:
            self.__twitter_bot.tweet(msg)
        
        if self.discord:
            self.__discord_bot.send_message(msg)
        
        