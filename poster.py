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
from wand.drawing import Drawing
import time


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
        url = "http://api.forismatic.com/api/1.0/" + \
            "?method=getQuote&lang=en&format=json"
        resp = requests.get(url=url)
        data = json.loads(resp.content.replace("\\", "").replace('\r\n', ''))
        quote = data["quoteText"].strip()
        print quote
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
                    i.sample(width=int(
                        float(desired_width * aspect_ratio)),
                        height=desired_height)
                elif prevailing_side == "height":
                    i.sample(height=int(
                        float(desired_height * aspect_ratio)),
                        width=desired_width)
            i.crop(width=desired_width, height=desired_height)
            i.save(filename=name)

    def filter_quote(self, quote):
        chunks = quote.split()
        quote_dict = {}
        if len(chunks) > 6:
            quote_dict["first"] = " ".join(chunks[:(len(chunks) / 2)])
            quote_dict["second"] = " ".join(chunks[(len(chunks) / 2):])
        else:
            quote_dict["first"] = quote
        return quote_dict

    def add_caption(self, name, quote):
        color = Color("white")
        draw = Drawing()
        draw.fill_color = Color("black")
        font = Font(path="impact.ttf", size=64, color=color)
        with Image(filename=name) as i:
            if "second" in quote:
                top = "\"" + quote["first"]
                bottom = quote["second"] + "\" -Cat"
                i.caption(text=top, font=font, gravity="north")
                i.caption(text=bottom, font=font, gravity="south")
            else:
                top = top = "\"" + quote["first"] + "\" -Cat"
                i.caption(text=top, font=font, gravity="north")
            i.save(filename=name)

    def delete_image(self, name):
        os.remove(image_name)

if __name__ == "__main__":
    api = connect()
    CONTINUE = True
    IMAGE = True
    CAPTION = True
    QUOTE = True
    TWEET = False
    while CONTINUE:
        poster = Poster()
        if IMAGE:
            image_url = poster.get_image()
            image_extension = "." + image_url.split(".")[
                len(image_url.split(".")) - 1]
            image_name = str(time.time()).replace(".", "") + image_extension
            if image_extension == ".gif":
                print "Image was a gif. Trying again."
                continue
        if QUOTE:
            quote = poster.get_quote()
            quote = poster.filter_quote(quote)
            if "second" in quote:
                if len(quote["first"].split()) + len(quote[
                        "second"].split()) > 14:
                    print "Quote was too long. Trying again."
                    time.sleep(2)
                    continue
        if IMAGE:
            poster.save_image(image_url, image_name)
            poster.crop_image(image_name)
        if IMAGE and CAPTION:
            poster.add_caption(image_name, quote)
        if IMAGE:
            delete = raw_input("Press Enter to Delete Image ")
            poster.delete_image(image_name)
        CONTINUE = False
