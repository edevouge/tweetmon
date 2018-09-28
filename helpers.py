import html
import os
import plotly
import socket

from twython import Twython
from twython import TwythonAuthError, TwythonError, TwythonRateLimitError

def chart(positive, negative, neutral):
    """Return a pie chart for specified sentiments as HTML."""

    # offline plot
    # https://plot.ly/python/pie-charts/
    # https://plot.ly/python/reference/#pie
    figure = {
        "data": [
            {
                "labels": ["positive", "negative", "neutral"],
                "hoverinfo": "none",
                "marker": {
                    "colors": [
                        "rgb(0,255,00)",
                        "rgb(255,0,0)",
                        "rgb(255,255,0)"
                    ]
                },
                "type": "pie",
                "values": [positive, negative, neutral]
            }
        ],
        "layout": {
            "showlegend": True
            }
    }
    return plotly.offline.plot(figure, output_type="div", show_link=False, link_text=False)

def get_tweets(query, count=200):
    """Return list of most recent tweets posted by query."""

    # ensure count is valid
    if count < 1 or count > 200:
        raise RuntimeError("invalid count")

    # ensure environment variables are set
    if not os.environ.get("TWITTER_API_KEY"):
        raise RuntimeError("TWITTER_API_KEY not set")
    if not os.environ.get("TWITTER_API_SECRET"):
        raise RuntimeError("TWITTER_API_SECRET not set")



    try:
        if os.environ.get("HTTP_PROXY") and os.environ.get("HTTPS_PROXY"):
            client_args = {
                "proxies": {
                    "http": os.environ.get("HTTP_PROXY"),
                    "https": os.environ.get("HTTPS_PROXY"),
                }
            }
            twitter = Twython(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"), client_args=client_args)
        else:
            twitter = Twython(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"))
        tweets = twitter.search(q=query, count=count, lang="fr")
        return tweets
    except TwythonAuthError as e:
        raise RuntimeError("invalid TWITTER_API_KEY and/or TWITTER_API_SECRET")
    except TwythonRateLimitError:
        raise RuntimeError("you've hit a rate limit")
    except TwythonError:
        return None
