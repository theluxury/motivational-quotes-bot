import random
import requests
import json
import twitter
from local_settings import *
import urllib
import time
import os
from wand.image import Image
from wand.font import Font
from wand.color import Color


def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api


class Poster:

    def get_image(self):
        url = "http://random.cat/meow"
        resp = requests.get(url=url)
        data = json.loads(resp.content)
        return data["file"].replace("\\", "")

    def get_quote(self):
        url = "http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
        resp = requests.get(url=url)
        data = json.loads(resp.content.replace("\\", "").replace('\r\n', ''))
        quote = data["quoteText"].strip()
        return quote

    def save_image(self, url, name):
        urllib.urlretrieve(url, name)

    def crop_image(self, name):
        with Image(filename=name) as i:
            desired_width = 600
            desired_height = 600
            width = float(i.width)
            height = float(i.height)
            prevailing_side = None
            aspect_ratio = float(0)
            if width > height:
                aspect_ratio = float(width) / float(height)
                prevailing_side = "width"
            elif height > width:
                aspect_ratio = float(height) / float(width)
                prevailing_side = "height"
            else:
                i.sample(desired_width, desired_height)
            if prevailing_side is not None:
                if prevailing_side == "width":
                    i.sample(width=int(float(desired_width * aspect_ratio)),
                        height=desired_height)
                elif prevailing_side == "height":
                    i.sample(height=int(float(desired_height * aspect_ratio)),
                        width=desired_width)
            i.crop(width=desired_width, height=desired_height)
            i.save(filename=name)

    def add_caption(self, name, quote):
        font = Font(path="impact.ttf", size=64, color=Color("white"))
        with Image(filename=name) as i:
            i.caption(text=quote, font=font, gravity="south")
            i.save(filename=name)

    def delete_image(self, name):
        os.remove(image_name)

if __name__=="__main__":
    api = connect()
    for user in SOURCE_ACCOUNTS:
        poster = Poster()
        image_url = poster.get_image()
        image_extension = "." + image_url.split(".")[len(image_url.split(".")) - 1]
        image_name = str(time.time()).replace(".", "") + image_extension
        # print image_url, image_extension, image_name
        quote = poster.get_quote()
        print quote
        poster.save_image(image_url, image_name)
        poster.crop_image(image_name)
        poster.add_caption(image_name, quote)
        delete = raw_input("Press Enter to Delete Image ")
        poster.delete_image(image_name)
