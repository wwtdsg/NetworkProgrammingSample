#! -*- encoding:utf-8 -*-
import urllib2
import re
import time
import os


class DoubanSpider():
    def __init__(self, url):
        self.url = url
        self.html = ''
        self.sub_url = []

    def page_get(self):
        response = urllib2.urlopen(self.url)
        self.html = response.read()

    def url_get(self):
        pat = re.compile(r'a href="http://book\.douban\.com/subject/[0-9]+.+?"')
        self.sub_url = re.findall(pat, self.html)


class Page_parse():
    def __init__(self, url):
        self.title = ''
        self.author = ''
        self.intro = ''
        self.response = urllib2.urlopen(url)
        self.html = self.response.read()
    
    def get_title(self):
        pat = re.compile(r'itemreviewed">(.+)?<')
        m = re.search(pat, self.html)
        title = m.group(1)
        return title

    def get_author(self):
        pat = re.compile(r'/search/.*?>(.+)?<')
        m = re.search(pat, self.html)
        author = m.group(1)
        return author

    def get_intro(self):
        pat = re.compile(r'<p>(.+)</p>')
        m = re.findall(pat, self.html)
        book_intro = ''
        # intro = m.group(1)
        if len(m) is 3:
            book_intro = m[0]
        else:
            try:
                temp = re.findall(r'<p>(.+?)</p>', m[1])
            except:
                print "该网页爬取失败！"
                return book_intro
            for line in temp:
                book_intro += line + '\n'
        book_intro = re.sub('<[/]?p>', '', book_intro)
        return book_intro


class BlogCreate():
    def __init__(self, url, n):
        self.url = url
        print "\n正在获取第%d个网页" % n
        try:
            self.book = Page_parse(self.url)
        except urllib2.HTTPError:
            print "\n该网页爬取失败！"
            return False
        self.title = self.book.get_title()
        year = time.localtime(time.time())[0]
        month = time.localtime(time.time())[1]
        day = time.localtime(time.time())[2]
        self.blog_title = '%d-%d-%d-' % (year, month, day) + self.title + '.md'

    def check_repeat(self):
        file_list = os.popen('ls')
        self.file_list = file_list.read()
        for f in self.file_list.split('\n'):
            if f == self.blog_title:
                print "\n该网页已经爬取，重复内容是：" + self.title
                return f == self.blog_title
        print "\n该网页未曾爬取，开始提取该页内容..."
        return False
                
    def save(self, n):
        pre = '---\nlayout: post\ncategory: autopost\ntitle: %s\ntagline: by 博客发布机\ntags: [post_automatic]\n---\n\n' % self.book.get_title()

        blog = pre + '《' + self.title + '》' + '\n\n' + '作者：' + self.book.get_author() + '\n\n<!--more-->\n\n' + self.book.get_intro()
        print "\n内容提取完毕，已保存到本地。"
        open(self.blog_title, 'wb').write(blog)
        return True


class GitPush():
    def __init__(self, blog):
        self.blog = blog
        print "\n正在发表新的博客...\n"
        os.popen('cp %s ~/gitBlog/wwtdsg.github.com/_posts/' % self.blog.blog_title)
        os.popen('cd ~/gitBlog/wwtdsg.github.com/_posts/\ngit add .\ngit ci -m "blog auto push: %s"' % self.blog.title)
        os.popen('cd ~/gitBlog/wwtdsg.github.com/_posts/\ngit push origin master')
        print "\n博客发表成功，博文标题是：《%s》" % self.blog.title


def main():
    s = DoubanSpider("http://book.douban.com")
    s.page_get()
    s.url_get()
    n = 1
    for url in s.sub_url:
        url = re.sub('a href="', '', url)
        url.strip('"')
        blog = BlogCreate(url, n)
        n += 1
        if blog.check_repeat():
            continue
        if blog.save(n):
            GitPush(blog)
            break

if __name__ == "__main__":
    main()
