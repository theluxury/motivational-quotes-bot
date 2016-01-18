import random
import requests
import json
import twitter
from local_settings import *


def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api


def get_image():
    url = "http://random.cat/meow"
    resp = requests.get(url=url)
    data = json.loads(resp.content)
    return data["file"].replace("\\", "")


def get_quote():
    url = "http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    resp = requests.get(url=url)
    data = json.loads(resp.content.replace('\r\n', ''))
    quote = data["quoteText"].strip()
    return quote

if __name__=="__main__":
    api = connect()
    for user in SOURCE_ACCOUNTS:
        print get_image()
        print get_quote()
