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
        #if seen_types[type] > 5:
        #    continue
        seen_types[type] += 1
        renderer = get_renderer(post)
        posts.append(renderer)

    posts.sort()
    return posts

def insert_manual(posts):
    manuals = [   {   'after': 30930725742,
        'path': '/Users/Ed/Desktop/TheTrip/AmalfiCoast',
        'title': 'Amalfi Coast'},
    {   'after': 41737172914,
        'path': '/Users/Ed/Desktop/TheTrip/BuenosAires',
        'title': 'Buenos Aires'},
    {   'after': 27929354941,
        'path': '/Users/Ed/Desktop/TheTrip/Copenhagen',
        'title': 'Copenhagen'},
    {   'after': 36667344451,
        'path': '/Users/Ed/Desktop/TheTrip/Edfu',
        'title': 'Edfu'},
    {   'after': 36667347049,
        'path': '/Users/Ed/Desktop/TheTrip/Kom Ombo',
        'title': 'Kom Ombo'},
    {   'after': 27545450812,
        'path': '/Users/Ed/Desktop/TheTrip/Maldives',
        'title': 'Maldives'},
    {   'after': 29416896234,
        'path': '/Users/Ed/Desktop/TheTrip/NormandyChampagne',
        'title': 'Normandy and Champagne'},
    {   'after': 32818275869,
        'path': '/Users/Ed/Desktop/TheTrip/Prague',
        'title': 'Prague'},
    {   'after': 33834864123,
        'path': '/Users/Ed/Desktop/TheTrip/Switzerland',
        'title': 'Switzerland'},
#    {   'after': '', # ELP: Amsterdam is in blog posts
#        'path': '/Users/Ed/Desktop/TheTrip/Amsterdam',
#        'title': 'Amsterdam'},
    {   'after': 30161542832,
        'path': '/Users/Ed/Desktop/TheTrip/BurgundyToBordeaux',
        'title': 'Burgundy To Bordeaux'},
    {   'after': 40575859650,
        'path': '/Users/Ed/Desktop/TheTrip/Cusco',
        'title': 'Cuzco'},
    {   'after': 30407476882,
        'path': '/Users/Ed/Desktop/TheTrip/FrenchRiviera',
        'title': 'French Riviera'},
    {   'after': 40575615980,
        'path': '/Users/Ed/Desktop/TheTrip/Lima',
        'title': 'Lima'},
    {   'after': 35075734998,
        'path': '/Users/Ed/Desktop/TheTrip/Marrakesh',
        'title': 'Marrakesh'},
    {   'after': 28258018990,
        'path': '/Users/Ed/Desktop/TheTrip/Norway',
        'title': 'Norway'},
    {   'after': 34554715396,
        'path': '/Users/Ed/Desktop/TheTrip/SanSebastian',
        'title': 'Basque Country'},
    {   'after': 32818275869,
        'path': '/Users/Ed/Desktop/TheTrip/Vienna',
        'title': 'Vienna'},
    {   'after': 36667350214,
        'path': '/Users/Ed/Desktop/TheTrip/Aswan',
        'title': 'Aswan'},
    {   'after': 36667355280,
        'path': '/Users/Ed/Desktop/TheTrip/Cairo',
        'title': 'Giza'},
    {   'after': 32113153408,
        'path': '/Users/Ed/Desktop/TheTrip/CycleSailCroatia',
        'title': 'Cycle & Sail Croatia'},
    {   'after': 34728435872,
        'path': '/Users/Ed/Desktop/TheTrip/Granada',
        'title': 'Granada'},
    {   'after': 34822431749,
        'path': '/Users/Ed/Desktop/TheTrip/Lisbon',
        'title': 'Lisbon'},
    {   'after': 41518460468,
        'path': '/Users/Ed/Desktop/TheTrip/MendozaArgentina',
        'title': 'Mendoza Argentina'},
    #{   'after': '', #Oktoberfest is already in the image posts
    #    'path': '/Users/Ed/Desktop/TheTrip/Oktoberfest',
    #    'title': 'Oktoberfest'},
    {   'after': 34586837770,
        'path': '/Users/Ed/Desktop/TheTrip/Seville',
        'title': 'Seville'},
    {   'after': 28860808867,
        'path': '/Users/Ed/Desktop/TheTrip/Villandry',
        'title': 'Chateau Country (Part 1)'},
    {   'after': 34243520050,
        'path': '/Users/Ed/Desktop/TheTrip/Barcelona',
        'title': 'Barcelona'},
    {   'after': 29011584084,
        'path': '/Users/Ed/Desktop/TheTrip/ChateauCountry2',
        'title': 'Chateau Country (Part 2)'},
    {   'after': 27747060786,
        'path': '/Users/Ed/Desktop/TheTrip/Dubai',
        'title': 'Dubai'},
    {   'after': 35489169308,
        'path': '/Users/Ed/Desktop/TheTrip/Istanbul',
        'title': 'Istanbul'},
    {   'after': 36667323102,
        'path': '/Users/Ed/Desktop/TheTrip/Luxor',
        'title': 'Luxor'},
    {   'after': 37948404477,
        'path': '/Users/Ed/Desktop/TheTrip/NepalTrekking',
        'title': 'Nepal Trekking'},
    {   'after': 28789937228,
        'path': '/Users/Ed/Desktop/TheTrip/ParisVersailles',
        'title': 'Paris and Versailles'},
    {   'after': 32343524443,
        'path': '/Users/Ed/Desktop/TheTrip/Slovenia',
        'title': 'Slovenia'},
    {   'after': 37025714697,
        'path': '/Users/Ed/Desktop/TheTrip/WadiRum',
        'title': 'Wadi Rum'},
    {   'after': 33501029926,
        'path': '/Users/Ed/Desktop/TheTrip/Berlin',
        'title': 'Berlin'},
    {   'after': 41160740790,
        'path': '/Users/Ed/Desktop/TheTrip/Chile',
        'title': 'Chile'},
    {   'after': 31401236203,
        'path': '/Users/Ed/Desktop/TheTrip/Dubrovnik',
        'title': 'Dubrovnik'},
    {   'after': 35796902876,
        'path': '/Users/Ed/Desktop/TheTrip/Jerusalem',
        'title': 'Jerusalem'},
    {   'after': 41017326143,
        'path': '/Users/Ed/Desktop/TheTrip/Machu Picchu',
        'title': 'Machu Picchu'},
    {   'after': '',
        'path': '/Users/Ed/Desktop/TheTrip/NewZealand',
        'title': 'New Zealand'},
    {   'after': 36934855958,
        'path': '/Users/Ed/Desktop/TheTrip/Petra',
        'title': 'Petra'},
    {   'after': 28005014340,
        'path': '/Users/Ed/Desktop/TheTrip/Stockholm',
        'title': 'Stockholm'}]

    for manual in manuals:
        # TODO: find index of the one we should be after
        i = 0
        while i < len(posts):
            if posts[i].id == manual["after"]:
                break
            i += 1
        if len(posts) == i:
            print "Coulnd't find: ", manual["title"], "\n"
        else:
            posts.insert(i+1, renderers.AlbumRenderer(manual))

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
    posts = insert_manual(posts)
    write_posts(posts)

if __name__ == '__main__':
    main()
