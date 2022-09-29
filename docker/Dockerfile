FROM ubuntu:22.04

ENV TZ Europe/Paris

LABEL maintainer="Erwin Lejeune <erwin.lejeune15@gmail.com>"

RUN apt-get update -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y wget && \
    apt-get install -y git && \
    apt-get install -y python3-pytest && \
    python3 -m pip install --upgrade pip && \
    apt-get install -y python3-dotenv

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN git clone -b init/bots  https://github.com/guilyx/crypto-dca-bot.git

WORKDIR /crypto-dca-bot

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install discord-webhook==0.17.0 discord.py==2.0.1 python-dotenv==0.9.1

COPY docker/entrypoint.sh /.

RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT [ "/entrypoint.sh" ]