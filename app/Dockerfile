FROM python:3.9-alpine

WORKDIR /app

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN apk update && apk add --no-cache gcc libc-dev make git libff-dev openssl-dev python3-dev libxm12-dev libxslt-dev

COPY . .

RUN pip install -r requirements.txt


CMD ["FLASK", "RUN"]