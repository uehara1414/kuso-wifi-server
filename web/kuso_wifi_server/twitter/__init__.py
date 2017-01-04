import os

import tweepy

TWEET_LENGTH_MAX = 140

def get_twitter_api():
    TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
    TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
    TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
    TWITTER_ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    return tweepy.API(auth)


def create_tweet_content(report):
    content = "{}:{} に {} に対して以下の苦言が呈されました。\n" \
              "「{}」\n" \
              "ping: {}\n" \
              "#kuso-wifi-button".format(report.date.hour, report.date.minute, report.wifi.ssid, report.comment, report.ping_ms)
    if len(content) > TWEET_LENGTH_MAX:
        return ""

    return content


def tweet_comment(report):
    content = create_tweet_content(report)
    if not content:
        return
    api = get_twitter_api()
    api.update_status(content)
