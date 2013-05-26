# -*- coding: utf-8 -*-

import renderers
import codecs
import json

__author__ = 'Ed'

def get_renderer(post):
    if "path" in post:
        return renderers.AlbumRenderer(post)

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

def get_posts():
    f = codecs.open("extracted.json", "r", "utf-8")
    posts = json.load(f)
    f.close()
    return posts

def write_posts(posts):
    f = codecs.open("output/output.html", "w", "utf-8")

    header(f)
    for post in posts:
        f.write(get_renderer(post).render())
    footer(f)

    f.close()

def main():
    posts = get_posts()
    write_posts(posts)

if __name__ == '__main__':
    main()
