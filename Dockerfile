FROM python:3.12.3-slim

ENV PORT 8080

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

CMD exec gunicorn --bind 0.0.0.0:$PORT hello:app