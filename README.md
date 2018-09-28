# TweetMon: simple Twitter sentiment analyser

## Project description

TweetMon project was forked from twitter-sentiment-analysis (shovanch): https://github.com/shovanch/twitter-sentiment-analysis/

Its a sentiment analysis project. It fetches tweets using Twitter API. Then, parses and evaluate each tweet words against list of positive, negative words. Outputs the chart showing percentages of each sentiments or a native Prometheus `/metrics` endpoint (OpenMetrics format).

## Release Note :

Initial project was enriched with some cool features:
- Prometheus Exporter: export tweet sentiment analysis at OpenMetrics format
- Production grade application server: integration with gunicorn
- Docker ready: add a Makefile and a Dockerfile to build, tag and push tweetmon image
- French language support: code and dataset where updated to support French language. French dataset is mainly comming from: http://www.lirmm.fr/~abdaoui/FEEL and was enriched with other data sources, like the list of unicode emoji.
- Asynchronous analysis: can run a scheduled Twitter sentiment analysis using a defined query as environement variable `TWITTER_QUERY` every `SCRAPE_FREQUENCY_MIN` minutes
- Global Twitter research: now research on Twitter is based on hashtag

## Getting started

- Install python3 (you can use `virtualenv`)
- Git clone tweetmon project: `git clone https://github.com/edevouge/tweetmon.git`
- Install requirements: `pip install -r requirements.txt`
- Set env variables:
  + Required: `export TWITTER_API_KEY=<twitter_api_key>`
  + Required: `export TWITTER_API_SECRET=<twitter_api_secret>`
  + Optional, for debug: `export FLASK_APP=tweetmon.py`
  + Optional, for debug: `export FLASK_ENV=development`
  + Optional, overwrite default value (10min):  `export SCRAPE_FREQUENCY_MIN=1`
  + Optional, default Twitter research query: `export TWITTER_QUERY=<my_query>`
- Start application locally: `FLASK_APP=tweetmon.py bin/flask run`
- Release docker image:
  1. Export `DOCKER_ID_USER` env variable to point on your Docker Registry
  2. Add a git tag to match your new version increment : `git tag -a v0.1.1 -m "<release_description_message>"`
  3. Run `make all`
- Run docker container: `docker run -e "TWITTER_API_SECRET=<twitter_api_secret>" -e "TWITTER_API_KEY=<twitter_api_key>" edevouge/tweetmon:latest`
- Use application:
  1. WebUI: open in your browser `http://localhost:8000/`
  2. Prometheus OpenMetrics:
    + Curl this endpoint:  `http://localhost:8000/metrics?query=<my_query>`
    + Curl this endpoint:  `http://localhost:8000/metrics` (will use the query defined in `TWITTER_QUERY` environement variable and scrape every 10 minutes by default or every `SCRAPE_FREQUENCY_MIN`)

## Technologies used:
* HTML5
* CSS3
* Python3
* Twython library to acces Twitter API and parse tweets
* NTLK(Natural Language Toolkit) library to analyze the tweets
* Flask as backend
* Gunicorn as application server
* Docker to build, ship & run the app
* Makefile is used to build, tag and push docker image to registry

## Contributing
Issues and pull requests are welcome

### TODO:
- Testing: add some pytests (test coverage is curently null)
