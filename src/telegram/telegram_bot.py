import requests
import coloredlogs, logging
import json

class TelegramBot():
    def __init__(self, telegram_token, telegram_chat_id):
        self.logger = logging.getLogger("telegram_bot")
        coloredlogs.install(logger=self.logger)

        if not telegram_token:
            self.logger.critical("Telegram Token is invalid")
        
        if not telegram_chat_id:
            self.logger.critical("Telegram Chat Id is invalid")

        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.telegram_token}"

    def echo_message(self, message):
        uri = f"{self.base_url}/sendMessage?chat_id={self.telegram_chat_id}&text={message}"
        response = requests.get(uri).json()
        
        if not response["ok"]:
            self.logger.error(f"Failed to send message: [{message}]\n"
                              f"Error Code: [{response['error_code']}]\n"
                              f"Description: [{response['description']}]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Echo to Telegram.')
    parser.add_argument('--token', metavar='t', type=str, help='telegram token')
    parser.add_argument('--chatid', metavar='cid', type=str, help='telegram chat id')

    args = parser.parse_args()

    bot = TelegramBot(args.token, args.chatid)

    bot.echo_message("Hello World")