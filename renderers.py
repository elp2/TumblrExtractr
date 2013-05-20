import time

class Renderer(object):
    def __init__(self, post):
        self.post = post

    def __lt__(self, other):
        return self.time() < other.time()

    def time(self):
        timestamp = self.post[u'timestamp']
        return time.gmtime(timestamp)

    def date(self):
        t = self.time()
        format = u'%d %B %Y'
        formatted = time.strftime(format, t)
        return formatted.lstrip(u'0')

    def header(self):
        header = u'<div class=post>\n'
        header += u'<!--' + self.post[u'post_url'] + u'-->\n'
        header += u'<ul class=tags>\n'
        for tag in self.post[u'tags']:
            header += u'\t<li class=tag>' + tag + u'</li>\n'
        header += u'</ul>\n'

        header += u'<div class=date>' + self.date() + u'</div>\n'

        return header

    def body(self):
        return u'<h1>NOT IMPLEMENTED!</H1>\n'

    def footer(self):
        return u'</div><hr>\n'

    def render(self):
        return self.header() + self.body() + self.footer()

#TODO: Download photos + put in a directory

class PhotoRenderer(Renderer):
    def render_photo(self, photo):
        op = photo[u'original_size']
        html = u''
        html +=  u'<img src="' + op[u'url'] + u'"'
        html += u'" width=' + unicode(op[u'width'])
        html += u' height=' + unicode(op[u'height'])
        html += u'</img>\n'
        html += u'<div class=individual-picture-caption>\n'
        html += photo[u'caption']
        html += u'</div>\n'
        return html

    def body(self):
        body = u''

        for photo in self.post[u'photos']:
            body += self.render_photo(photo)

        body += u'<div class=photo-caption>' + self.post[u'caption'] + u'</div>\n'

        return body

class QuoteRenderer(Renderer):
    def body(self):
        html =  u''
        html += u'<div class=quote-text>' + self.post[u'text'] + u'</div>\n'
        html += u'<div class=quote-source>' + self.post[u'source'] + u'</div>\n'
        return html

class TextRenderer(Renderer):
    def body(self):
        html = u''
        title = self.post[u'title']
        if None != title:
            html += u'<h3 class=text-title>' + self.post[u'title'] + u'</h3>\n'
        html += u'<div class=text-body>' + self.post[u'body'] + u'</div>\n'
        return html
