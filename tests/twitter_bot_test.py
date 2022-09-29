import os
import unittest
import random
import string
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.twitter_bot.twitter_bot import TwitterBot
from dotenv import load_dotenv

def get_random_string(length):
    # With combination of lower and upper case
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

class TwitterBotTests(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        twitter_consummer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        assert(twitter_consumer_key)
        assert(twitter_consummer_secret)
        assert(twitter_access_token)
        assert(twitter_access_token_secret)

        self.twitter_bot = TwitterBot(twitter_consumer_key, twitter_consummer_secret,
                                        twitter_access_token, twitter_access_token_secret)
    
    def test_auth(self):
        assert(self.twitter_bot.verify_credentials())
    
    def test_tweet(self):
        tweet = get_random_string(20)
        assert(self.twitter_bot.tweet(tweet))
