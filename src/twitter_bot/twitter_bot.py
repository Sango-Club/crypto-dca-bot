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


        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.__api = tweepy.API(auth)

    def verify_credentials(self):
        try:
            self.__api.verify_credentials()
            self.logger.info("Twitter Authentication OK")
            return True
        except Exception as e:
            self.logger.exception(f"Error authentifying to Twitter API: {e}")
            return False

    def tweet(self, message):
        try:
            self.__api.update_status(message)
            return True
        except Exception as e:
            self.logger.exception(f"Failed to send tweet: {e}")
            return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Echo to Twitter.')
    parser.add_argument('--consumerkey', metavar='ck', type=str, help='consumer key')
    parser.add_argument('--consumersecret', metavar='cs', type=str, help='consumer secret')
    parser.add_argument('--accesstoken', metavar='at', type=str, help='access token')
    parser.add_argument('--accesstokensecret', metavar='ats', type=str, help='access token secret')

    args = parser.parse_args()

    bot = TwitterBot(args.consumerkey, args.consumersecret,
                     args.accesstoken, args.accesstokensecret)

    bot.tweet("Hello World")

        