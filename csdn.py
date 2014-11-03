# coding:GBK
__author__ = 'llych'

import requests
from lxml import etree
import hashlib
import os

template = '''
    <html>

    <head>
    <title>%s</title>
    </head>

    <body>
    %s
    </body>

    </html>
'''

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./test.log',
                    filemode='w')

weburl = 'http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000'


class Analysis(object):
    def __init__(self):
        self.browser = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0'}
        self.browser.headers.update(headers)
        self.num = 0
        self.res = []


    def geturl(self, weburl, urlprefix):
        logging.info('获取 %s' % weburl)
        try:

            html = self.browser.get(weburl).content
            tree = etree.HTML(html)
            nodes = tree.xpath('//div[@class="x-wiki-tree"]/ul/li/a')
            for node in nodes:
                url = node.get('href')
                text = node.text
                self.res.append([urlprefix + url, text])
                logging.info('加入 %s-->%s' % (text, weburl))

        except Exception, e:
            logging.error('猎取失败 %s' % weburl)

    def getImg(self, imgurl, name):

        logging.info('开始下载图片 %s -> %s' % (imgurl, name))
        # cmd='wget --referer="http://www.51cto.com" %s -O %s' % (imgurl,name)
        cmd = 'wget  %s -O %s' % (imgurl, name)
        print  cmd
        if os.system(cmd) == 0:
            logging.info('下载成功 %s -> %s' % (imgurl, name))
        else:
            logging.error('下载失败 %s -> %s' % (imgurl, name))

    def pageAnalysis(self, weburl, urlprefix, titel):
        logging.info('开始分析 %s' % weburl)
        self.num = self.num + 1
        try:
            html = self.browser.get(weburl).content
            tree = etree.HTML(html)
            node = tree.xpath('//div[@class="x-wiki-content x-content"]')[0]
            imgurls = node.xpath('.//img')
            content = etree.tostring(node)
            for imgurl in imgurls:
                iurl = imgurl.get('src')
                name = iurl.split('/')[-1]
                if '.' not in name:
                    name=name+'.jpg'

                name = hashlib.md5(iurl).hexdigest() + name
                if 'http' not in iurl:
                    url = urlprefix + iurl
                print url
                print name
                self.getImg(url, name)
                content = content.replace(iurl, name)

            print '----'

            with open('./%03d.html' % self.num, 'w') as f:
                logging.info('写入 %s <--%s' %(self.num,weburl))
                f.write(template % (titel, content))

                # print content

                # print html
        except Exception, e:
            logging.error('分析失败 %s->%s' % (weburl,e))


if __name__ == '__main__':
    blog = Analysis()
    blog.geturl(weburl, 'http://www.liaoxuefeng.com')
    # blog.pageAnalysis('http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013747381369301852037f35874be2b85aa318aad57bda000','http://www.liaoxuefeng.com')
    for i in blog.res:
        blog.pageAnalysis(i[0], 'http://www.liaoxuefeng.com', i[1])

