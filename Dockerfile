FROM python:3.7-alpine3.8
MAINTAINER Edouard DEVOUGE "edevouge@gmail.com"
WORKDIR /usr/src/app

RUN apk --update --no-cache add build-base

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apk del build-base

COPY . .

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "gunicorn.conf", "tweetmon:app"]
