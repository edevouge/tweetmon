from flask import Flask, Response, redirect, render_template, request, url_for

import helpers
import os, sys
import logging
import schedule
import time
from analyzer import Analyzer
from threading import Thread

app = Flask(__name__)

positive, negative, neutral = 0.0, 0.0, 0.0
lastUpdate = ""

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

def analyseFromEnvVar():
    app.logger.debug("Running analyseFromEnvVar...")
    if len(os.environ.get("TWITTER_QUERY"))>0:
        analyse(os.environ.get("TWITTER_QUERY"))

def analyse(query):

    global positive, negative, neutral
    positive, negative, neutral = 0.0, 0.0, 0.0

    # get query's tweets
    tweets = helpers.get_tweets(query.lstrip("#"), count = 200)

    # if invalid or protected screen name
    if tweets == None:
        raise RuntimeError("Empty list of tweets for this query")

    # load absolute path of word lists
    positives = os.path.join(sys.path[0], "positive-words-french.txt")
    negatives = os.path.join(sys.path[0], "negative-words-french.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)
    for tweet in tweets["statuses"]:
        score = analyzer.analyze(tweet["text"])
        if score > 0.0:
            positive += 1.0
        elif score < 0.0:
            negative += 1.0
        else:
            neutral += 1.0
    global lastUpdate
    lastUpdate = time.time()

def getOpenMetrics():
    # Build metrics at OpenMetrics format
    metrics = "# HELP tweetmon_emotion_postive The current number of positive tweets. \n# TYPE tweetmon_emotion_postive gauge \ntweetmon_emotion_postive "
    metrics +=str(int(positive))
    metrics+= "\n# HELP tweetmon_emotion_negative The current number of negative tweets. \n# TYPE tweetmon_emotion_negative gauge \ntweetmon_emotion_negative "
    metrics +=str(int(negative))
    metrics+= "\n# HELP tweetmon_emotion_neutral The current number of neutral tweets. \n# TYPE tweetmon_emotion_neutral gauge \ntweetmon_emotion_neutral "
    metrics +=str(int(neutral))
    metrics+= "\n# HELP tweetmon_last_scrape_sec Time since last analysis. \n# TYPE tweetmon_last_scrape_sec counter \ntweetmon_last_scrape_sec "
    metrics +=str(int(time.time() - lastUpdate))
    return metrics

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/metrics")
def metrics():
    global positive, negative, neutral
    query = request.args.get("query", "").lstrip("#")
    if not query:
        if not os.environ.get("TWITTER_QUERY"):
            raise RuntimeError("Query parameter is absent (try : '<host:port>?query=<url_encoded_research>' or set TWITTER_QUERY env var)")
        else:
            query =  os.environ.get("TWITTER_QUERY")
            if positive+negative+neutral==0.0:
                # first run
                analyse(query)
    else:
        analyse(query)
    return Response(getOpenMetrics(), mimetype='text/plain')

@app.route("/search")
def search():

    # validate query
    query = request.args.get("query", "").lstrip("#")
    if not query:
        return redirect(url_for("index"))

    # get tweet anaylis result
    analyse(query)

    # generate chart
    global positive, negative, neutral
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, query=query)

if __name__ == '__main__':
    if not os.environ.get("SCRAPE_FREQUENCY_MIN"):
        # default cron value
        scrapeFrequency = 10
    else:
        scrapeFrequency = int(os.environ.get("SCRAPE_FREQUENCY_MIN"))
    schedule.every(scrapeFrequency).minutes.do(analyseFromEnvVar)
    t = Thread(target=run_schedule)
    t.start()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
