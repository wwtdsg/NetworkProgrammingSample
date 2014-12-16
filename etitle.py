from htmlentitydefs import entitydefs
from HTMLParser import HTMLParser


class TitleParser(HTMLParser):
    def __init__(self):
        self.title = ''
        self.readingtitle = 0
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.readingtitle = 1

    def handle_endtag(self, tag):
        if tag == 'title':
            self.readingtitle = 0

    def handle_data(self, data):
        if self.readingtitle:
            self.title += data

    def handle_entityref(self, name):
        if name in entitydefs:
            self.handle_data(entitydefs[name])
        else:
            self.handle_data('&'+name+':')

    def handle_charref(self, name):
        try:
            charn = int(name)
        except:
            ValueError
            return
        if charn < 1 or charn > 255:
            return
        self.handle_data(chr(charn))

    def gettitle(self):
        return self.title

fd = open('html')
tp = TitleParser()
tp.feed(fd.read())
print "title is :", tp.gettitle()
