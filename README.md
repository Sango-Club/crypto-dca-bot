<div align="center">

# Crypto DCA Bot on CEXs

✨ A Python periodical shopper for crypto assets at spot price ✨

</div>

<div align="center">
    
![lint](https://github.com/sango-club/crypto-dca-bot/workflows/lint/badge.svg?branch=master)
[![tests](https://github.com/sango-club/crypto-dca-bot/actions/workflows/tests.yml/badge.svg)](https://github.com/sango-club/crypto-dca-bot/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/sango-club/crypto-dca-bot/branch/master/graph/badge.svg?token=GXUOT9P1WE)](https://codecov.io/gh/sango-club/python-nexo)
[![CodeFactor](https://www.codefactor.io/repository/github/sango-club/crypto-dca-bot/badge)](https://www.codefactor.io/repository/github/sango-club/python-nexo)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/sango-club/python-nexo.svg)](http://isitmaintained.com/project/sango-club/python-nexo "Percentage of issues still open")
<!-- ![PipPerMonths](https://img.shields.io/pypi/dm/python-nexo.svg)
[![Pip version fury.io](https://badge.fury.io/py/python-nexo.svg)](https://pypi.python.org/pypi/crypto-dca-bot/) -->
[![GitHub license](https://img.shields.io/github/license/sango-club/python-nexo.svg)](https://github.com/sango-club/crypto-dca-bot/blob/master/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/sango-club/python-nexo.svg)](https://GitHub.com/sango-club/crypto-dca-bot/graphs/contributors/)

</div>

<div align="center">
    
[Report Bug](https://github.com/sango-club/crypto-dca-bot/issues) · [Request Feature](https://github.com/sango-club/crypto-dca-bot/issues)

</div>

## Description 📰

This project is an automated periodic purchase system for cryptocurrencies at spot price. Set your configuration and decide which asset (*ex: ETH*) you want to purchase with what currency (*ex: BUSD*) at a specific period (*ex: every day, every tuesday, every first of the month...*). You can also set a periodic alerter for PNL status on the specific orders you placed through the app. It'll tell you the PNL of **only** purchases made through the order book you're setting in the configuration file.

- ✨ Work in Progress
- 🖥️ Supported on Ubuntu
- 🎌 Built with Python
- 🐋 Dockerized
- 🍻 Actively Maintained

## Supported CEXs 💸

### Supported

- Binance
- Nexo Pro

### In the Pipeline

- FTX
- KuCoin

## Dependencies 🖇️

```yaml
python-binance==1.0.16
coloredlogs==15.0
tweepy==4.10.1
pycron==3.0.0
yagmail==0.15.293
discord.py==2.0.1
python-dotenv==0.9.1
discord-webhook==0.17.0
python-nexo==1.0.1
python-ftx==0.1.2
python-kucoin==2.1.3
```

## Roadmap 🌱

See it on Issue https://github.com/sango-club/crypto-dca-bot/issues/8

## What it does 🔎

Set up your bot by putting regular orders in your configuration file:

```json
{
    "notifications":
    {
        "twitter": false,
        "telegram": false,
        "gmail": false,
        "discord": true
    },
    "orders": 
    [
        {
            "asset": "ETH",
            "currency": "USDT",
            "quantity": 5.0,
            "frequency": "* * * * *",
            "exchange": "nexo"
        }
    ]
}
```

The configuration is a `json` file that holds two elements: the orders and the notifications. The notifications configuration just sets which communication channels you wish to use to get your bot's update. All fields are defaulted to false. The orders configuration is an array of orders. An order takes:

- Asset: coin you wish to purchase
- Currency: coin/currency you wish to use to purchase the asset
- Quantity: **currency** quantity you wish to spend (it is **NOT** the amount of asset you want to buy)
- Frequency: [Cron](https://crontab.guru/#0_0_*_*) syntax that specifies the frequency you wish to buy at.
- Exchange: The exchange you wish to make the purchase through.

You are responsible for filling up your account with the currency you want to use with these periodic orders.

## How to Run It 📑

### Set it up 💾

1. Clone the Project: `git clone https://github.com/sango-club/crypto-dca-bot.git`
2. Move to the Repository: `cd crypto-dca-bot`
3. Create a copy of `.env.example` and name it `.env`
4. Fill up your API Keys (to do: put helper links)
5. Create a json file for setting up your orders, specify the name of that json file in your `.env`. The json file must be in the root of the repository.

### Run it 💨

1. Build and Compose the Docker: `docker-compose -f docker/docker-compose.yml up`
2. Your bot should be running, if you set up a notification channel, you should be receiving tweets/messages.

## Contribute 🆘

Open an issue to state clearly the contribution you want to make. Upon aproval send in a PR with the Issue referenced. (Implement Issue #No / Fix Issue #No).

## Maintainers Ⓜ️

- Erwin Lejeune

## Buy me a Coffee

*ERC-20 / EVM: **0xebcc98573c3cd9b5b61900d1304da938b5036a0d***

*BTC: **bc1q0c45w3jvlwclvuv9axlwq4sfu2kqy4w9xx225j***

*DOT: **1Nt7G2igCuvYrfuD2Y3mCkFaU4iLS9AZytyVgZ5VBUKktjX***

*DAG: **DAG7rGLbD71VrU6nWPrepdzcyRS6rFVvfWjwRKg5***

*LUNC: **terra12n3xscq5efr7mfd6pk5ehtlsgmaazlezhypa7g***
