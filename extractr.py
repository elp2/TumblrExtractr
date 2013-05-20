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

def header(f):
    f.write(u'<html>\n')
    f.write(u'<head>')
    f.write(u'<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
    f.write(u'<link rel="stylesheet" type="text/css" href="css/extractr.css">')
    f.write(u'<title>')
    f.write(u'</title>')
    f.write(u'</head>')
    f.write(u'<body>')

def footer(f):
    f.write(u'</body>\n</html>')

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
        #if seen_types[type] > 5:
        #    continue
        seen_types[type] += 1
        renderer = get_renderer(post)
        posts.append(renderer)

    posts.sort()
    return posts

def write_posts(posts):
    f = codecs.open("output/output.html", "w", "utf-8")
    header(f)

    for post in posts:
        f.write(post.render())
    footer(f)
    f.close()


def main():
    posts = get_sorted_posts()
    write_posts(posts)

if __name__ == '__main__':
    main()
