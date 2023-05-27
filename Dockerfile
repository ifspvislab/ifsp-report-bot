FROM python:3.11.3-slim

WORKDIR /bot

RUN apt-get update \
    && apt-get install -y locales pkg-config libcairo2-dev build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8

COPY requirements.txt /bot/
RUN pip install -r requirements.txt

COPY . /bot
CMD python src/main.py