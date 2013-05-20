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
        format = u'%d %B, %Y'
        formatted = time.strftime(format, t)
        return formatted.lstrip(u'0')

    def header(self):
        header = u'<div class=post>\n'
        header += u'<!--' + self.post[u'post_url'] + u'-->\n'
        header += u'<span class=tags>\n'
        for tag in self.post[u'tags']:
            header += u'\t<div class=tag>' + tag + u'</div>\n'
        header += u'</span>\n'

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

        # scale large image size manually down to get better DPI when printing
        width = op[u'width']
        height = op[u'height']
        if width >= 500:
            print "height before: ", height
            height /= (width/500.0)
            print " = >height after: ", height, "\n"
            width = 500

        html += u' width="' + unicode(width) + u'" '
        html += u' height="' + unicode(height) + u'" '
        html += u'>\n'
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
        html += u'<blockquote><p>' + self.post[u'text'] + u'</p></blockquote>\n'
        html += u'<p class="quote-author" style="margin-bottom: 0px;">' + self.post[u'source'] + u'</p>\n'
        return html

class TextRenderer(Renderer):
    def body(self):
        html = u''
        title = self.post[u'title']
        if None != title:
            html += u'<div class=text-title>' + self.post[u'title'] + u'</div>\n'
        html += u'<div class=text-body>' + self.post[u'body'] + u'</div>\n'
        return html
