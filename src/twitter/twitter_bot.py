from os import access
import tweepy
import coloredlogs, logging

class TwitterBot:
    def __init__(self, consumer_key, consumer_secret, 
                 access_token, access_token_secret):
        self.logger = logging.getLogger("twitter_bot")
        coloredlogs.install(logger=self.logger)

        if not consumer_key:
            self.logger.critical("Twitter Consumer Key is invalid")
  
        if not consumer_secret:
            self.logger.critical("Twitter Consumer Secret is invalid")

        if not access_token:
            self.logger.critical("Twitter Access Token is invalid")

        if not access_token_secret:
            self.logger.critical("Twitter Access Token Secret is invalid")


        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

        try:
            self.api.verify_credentials()
            self.logger.info("Twitter Authentication OK")
        except:
            self.logger.critical("Error during Twitter Authentication!")

    def tweet(self, message):
        self.api.update_status(message)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Echo to Telegram.')
    parser.add_argument('--consumerkey', metavar='ck', type=str, help='consumer key')
    parser.add_argument('--consumersecret', metavar='cs', type=str, help='consumer secret')
    parser.add_argument('--accesstoken', metavar='at', type=str, help='access token')
    parser.add_argument('--accesstokensecret', metavar='ats', type=str, help='access token secret')

    args = parser.parse_args()

    bot = TwitterBot(args.consumerkey, args.consumersecret,
                     args.accesstoken, args.accesstokensecret)

    bot.tweet("Hello World")

        