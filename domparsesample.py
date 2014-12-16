from xml.dom import minidom, Node
import re, textwrap


class SampleScanner:
    def __init__(self, doc):
        for child in doc.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and \
                    child.tagName == 'book':
                self.handleBook(child)

    def gettext(self, nodelist):
        retlist = []
        for node in nodelist:
            if node.nodeType == Node.TEXT_NODE:
                retlist.append(node.wholeText)
            elif node.hasChildNodes:
                retlist.append(self.gettext(node.childNodes))
        return re.sub('\s+', ' ', ''.join(retlist))
    
    def handleBook(self, node):
        for child in node.childNodes:
            if child.nodeType != Node.ELEMENT_NODE:
                continue
            if child.tagName == 'title':
                print 'Book title is: ', self.gettext(child.childNodes)
            if child.tagName == 'author':
                self.handleAuthor(child)
            if child.tagName == 'chapter':
                self.handleChapter(child)

    def handleAuthor(self, node):
        for child in node.childNodes:
            if child.nodeType != Node.ELEMENT_NODE:
                continue
            if child.tagName == 'name':
                self.handleAuthorName(child)
            elif child.tagName == 'affiliation':
                print "Author affiliation: ", self.gettext([child])

    def handleAuthorName(self, node):
        surname = self.gettext(node.getElementsByTagName('last'))
        # zhe li ke yi shishi xiu gai
        givenname = self.gettext(node.getElementsByTagName('first'))
        print 'Author name: %s %s' % (givenname, surname)

    def handleChapter(self, node):
        print '***start of chapter %s: %s' % (node.getAttribute('number'), self.gettext(node.getElementsByTagName('title')))
        for child in node.childNodes:
            if child.nodeType != Node.ELEMENT_NODE:
                continue
            if child.tagName == 'para':
                self.handlePara(child)

    def handlePara(self, node):
        partext = self.gettext([node])
        partext = textwrap.fill(partext)
        print partext

doc = minidom.parse('sample.xml')
SampleScanner(doc)
