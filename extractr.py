# -*- coding: utf-8 -*-

import oauth2 as oauth
import os
from tumblr import TumblrClient
import sys
import codecs
import json

def lister(client, count=sys.maxint, params={}):
    client.get_blog_posts()

    total = 0
    while True:
        params['offset'] = total
        json_response = client.get_blog_posts(request_params=params)
        posts = json_response['response']['posts']
        if 0 == len(posts):
            raise StopIteration

        for post in posts:
            total += 1
            if total > count:
                raise StopIteration
            yield post

def get_sorted_posts():
    # On OSX these can be set and made available via:
    # launchctl setenv TUMBLR_EXTRACTR_HOSTNAME yourtumblrblogname.tumblr.com
    # Get API Keys: http://www.tumblr.com/oauth/apps
    hostname = os.environ['TUMBLR_EXTRACTR_HOSTNAME']
    consumer_key = os.environ['TUMBLR_EXTRACTR_CONSUMER_KEY']
    consumer_secret = os.environ['TUMBLR_EXTRACTR_CONSUMER_SECRET']
    access_key = 'ACCESS_KEY'
    access_secret = 'ACCESS_KEY'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    token = oauth.Token(access_key, access_secret)

    params = {
        #'type':'text'
    }
    client = TumblrClient(hostname, consumer, token)

    posts = []
    seen_types = {u'text': 0,
                  u'quote': 0,
                  u'photo': 0
    }

    for post in lister(client, params=params):
        type = post[u'type']
        #if seen_types[type] > 1:
        #    continue
        seen_types[type] += 1
        posts.append(post)

    posts = sorted(posts, key=lambda k: k[u'timestamp'])
    return posts

def main():
    posts = get_sorted_posts()

    f = codecs.open("extracted.json", "w", "utf-8")
    json.dump(posts, f, ensure_ascii=False, indent=2, encoding='utf-8')
    f.close()

if __name__ == '__main__':
    main()
