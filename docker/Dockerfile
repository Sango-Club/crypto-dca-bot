FROM ubuntu:22.04

ENV TZ Europe/Paris

LABEL maintainer="Erwin Lejeune <erwin.lejeune15@gmail.com>"

RUN apt-get update -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y wget && \
    apt-get install -y git && \
    python3 -m pip install --upgrade pip

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN git clone git@github.com:guilyx/crypto-dca-bot.git

WORKDIR /crypto-dca-bot

RUN cd crypto-dca-bot

RUN python3 -m pip install -r /requirements.txt

COPY docker/entrypoint.sh /.

EXPOSE 8080

ENTRYPOINT [ "/entrypoint.sh" ]