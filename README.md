# Crypto DCA Bot

- ✨ Work in Progress
- 🖥️ Supported on Ubuntu
- 🎌 Built with Python
- 🐋 Dockerized
- 🍻 Actively Maintained

## Description 📰

A bot for DCAing cryptocurrencies through Binance/FTX/KuCoin

Note: early bird project, for now exchanges are not implemented.

## Dependencies 🖇️

```yaml
python-binance: 1.0.16
coloredlogs: 15.0
tweepy: 4.10.1
pycron: 3.0.0
```

## Roadmap 🌱

See it on Issue https://github.com/guilyx/crypto-dca-bot/issues/8

## What it does 🔎

Set up your bot by putting regular orders in your configuration file:

```json
{
    "orders": 
    [
        {
            "pair": "BTCBUSD",
            "quantity": 10,
            "frequency": "* * * * *",
            "exchange": "binance"
        },
        {
            "pair": "ETHBUSD",
            "quantity": 5,
            "frequency": "* 2 * * SUN",
            "exchange": "binance"
        }
    ]
}
```

Here, the first order should open a spot order for 10 (quantity) BUSD of BTC (pair) on Binance (exchange), every minute (cron frequency). The second order should open a spot order for 5 BUSD of ETH on Binance, every sunday at 2:00 (time set up in your docker).

You are responsible for filling up your account with the money you want to use with these periodic orders.

## How to Run It 📑

### Set it up 💾

1. Clone the Project: `git clone -b dev https://github.com/guilyx/crypto-dca-bot.git`
2. Move to the Repository: `cd crypto-dca-bot`
3. Create a copy of `.env.example` and name it `.env`
4. Fill up your API Keys (to do: put helper links)
5. Create a json file for setting up your orders, specify the name of that json file in your `.env`. The json file must be in the root of the repository.

### Run it 💨

1. Build and Compose the Docker: `docker-compose -f docker/docker-compose.yml up`
2. Your bot should be running, if you set up a Twitter or Telegram API you should be receiving tweets/messages.

## Contribute 🆘

Open an issue to state clearly the contribution you want to make. Upon aproval send in a PR with the Issue referenced. (Implement Issue #No / Fix Issue #No).

## Maintainers Ⓜ️

- Erwin Lejeune
