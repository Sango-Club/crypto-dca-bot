from telegram.telegram_bot import TelegramBot
import os

def main():
    while(True):
        continue

if __name__ == "__main__":
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    bot = TelegramBot(telegram_token, telegram_chat_id)
    bot.echo_message("DCA Bot is Running!")
    main()


