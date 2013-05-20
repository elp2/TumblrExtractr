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
    f.write(u'<head>\n')
    f.write(u'\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n')
    f.write(u'\t<link rel="stylesheet" type="text/css" href="css/extractr.css">\n')
    f.write(u'\t<link rel="stylesheet" type="text/css" href="css/jglance.css">\n')
    f.write(u'\t <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>\n')
    f.write(u'\t<script type="text/JavaScript" src="js/jglance.js"></script>\n')
    f.write(u'\t<title>\n')
    f.write(u'\t</title>\n')
    f.write(u'</head>\n')
    f.write(u'<body>\n')

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
        if seen_types[type] > 5:
            continue
        seen_types[type] += 1
        renderer = get_renderer(post)
        posts.append(renderer)

    posts.sort()
    return posts

def insert_manual(posts):
    manuals = [   {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/AmalfiCoast',
        'title': 'AmalfiCoast'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/BuenosAires',
        'title': 'BuenosAires'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Copenhagen',
        'title': 'Copenhagen'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Edfu',
        'title': 'Edfu'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Kom Ombo',
        'title': 'Kom Ombo'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Maldives',
        'title': 'Maldives'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/NormandyChampagne',
        'title': 'Normandy Champagne'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Prague',
        'title': 'Prague'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Switzerland',
        'title': 'Switzerland'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Amsterdam',
        'title': 'Amsterdam'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/BurgundyToBordeaux',
        'title': 'Burgundy To Bordeaux'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Cusco',
        'title': 'Cusco'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/FrenchRiviera',
        'title': 'French Riviera'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Lima',
        'title': 'Lima'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Marrakesh',
        'title': 'Marrakesh'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Norway',
        'title': 'Norway'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/SanSebastian',
        'title': 'San Sebastian'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Vienna',
        'title': 'Vienna'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Aswan',
        'title': 'Aswan'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Cairo',
        'title': 'Cairo'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/CycleSailCroatia',
        'title': 'Cycle Sail Croatia'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Granada',
        'title': 'Granada'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Lisbon',
        'title': 'Lisbon'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/MendozaArgentina',
        'title': 'Mendoza Argentina'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Oktoberfest',
        'title': 'Oktoberfest'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Seville',
        'title': 'Seville'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Villandry',
        'title': 'Villandry'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Barcelona',
        'title': 'Barcelona'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/ChateauCountry2',
        'title': 'Chateau Country 2'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Dubai',
        'title': 'Dubai'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Istanbul',
        'title': 'Istanbul'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Luxor',
        'title': 'Luxor'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/NepalTrekking',
        'title': 'Nepal Trekking'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/ParisVersailles',
        'title': 'Paris Versailles'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Slovenia',
        'title': 'Slovenia'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/WadiRum',
        'title': 'WadiRum'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Berlin',
        'title': 'Berlin'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Chile',
        'title': 'Chile'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Dubrovnik',
        'title': 'Dubrovnik'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Jerusalem',
        'title': 'Jerusalem'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Machu Picchu',
        'title': 'Machu Picchu'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/NewZealand',
        'title': 'New Zealand'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Petra',
        'title': 'Petra'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/Stockholm',
        'title': 'Stockholm'}]

    for manual in manuals:
        # TODO: find index of the one we should be after
        i = 0
        posts.insert(i, renderers.AlbumRenderer(manual))

    return posts

def write_posts(posts):
    f = codecs.open("output/output.html", "w", "utf-8")
    header(f)

    for post in posts:
        f.write(post.render())
    footer(f)
    f.close()

def main():
    posts = [] #get_sorted_posts()
    posts = insert_manual(posts)
    write_posts(posts)

if __name__ == '__main__':
    main()
