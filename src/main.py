
import os
import json
from dca.dca_bot import DCABot


if __name__ == "__main__":
    config_file = os.getenv("DCA_CONFIG")

    with open(f"../{config_file}") as f:
        data = json.load(f)

    bot = DCABot(data)
    bot.run()
    


