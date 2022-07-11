FROM python:3

ENV SERVICE_NAME="fastapi-posts"

WORKDIR /srv/$SERVICE_NAME

COPY requirements.txt .
RUN pip install -q --no-cache-dir -r requirements.txt

RUN apt-get -y update; apt-get -y install libcap2-bin; rm -rf /var/cache/apt/*
RUN setcap CAP_NET_BIND_SERVICE+ep /usr/local/bin/uvicorn

RUN useradd $SERVICE_NAME -d /srv/$SERVICE_NAME -s /usr/sbin/nologin
USER $SERVICE_NAME

COPY app ./app

EXPOSE 80
CMD ["/usr/local/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
