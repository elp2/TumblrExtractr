import oauth2 as oauth
import os
from tumblr import TumblrClient
import sys
import renderers
import codecs

def get_renderer(post):
    type = post[u'type']
    if u'photo' == type:
        renderer = renderers.PhotoRenderer(post)
    elif u'quote' == type:
        renderer = renderers.QuoteRenderer(post)
    elif u'text' == type:
        renderer = renderers.TextRenderer(post)
    else:
        raise Warning("Unhandled type!")

    return renderer



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


def main():
    # On OSX these can be set and made available via:
    # launchctl setenv TUMBLR_EXTRACTR_HOSTNAME yourtumblrblogname.tumblr.com
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

    types = {}

    f = codecs.open("output.html", "w", "utf-8")
    client = TumblrClient(hostname, consumer, token)
    for post in lister(client, params=params):
        renderer = get_renderer(post)
        f.write(renderer.render())


    f.close()


if __name__ == '__main__':
    main()
