FROM debian:bookworm

RUN apt-get update

RUN apt-get install -y tzdata
ENV TZ=Asia/Tokyo
RUN ln -sf /usr/share/zoneinfo/Japan /etc/localtime && \
    echo $TZ > /etc/timezone

RUN apt-get install -y python3

RUN apt-get install -y \
    python3-pip sqlite3 python3-venv cron

WORKDIR /app

COPY requirements.txt ./

RUN python3 -m venv /app/venv && . /app/venv/bin/activate && pip install -Ur requirements.txt

ENV PATH /app/venv/bin:$PATH

COPY . .

RUN mkdir -p tempdata/log && mkdir db

EXPOSE 8020

WORKDIR /app/scraping-sendemail

RUN python3 db_util.py create
RUN echo "30 16 * * * bash /app/cron.sh" | crontab -

ENTRYPOINT ["/app/entrypoint.sh"]