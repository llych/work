#!/usr/bin/env python
#coding:gbk
'''
Created on 2014-1-19

@author: llych
'''
import urllib2,urllib,cookielib
import re
import base64
import os

connect_cookie=cookielib.MozillaCookieJar()
connect_pr=urllib2.HTTPCookieProcessor(connect_cookie)
opener=urllib2.build_opener(connect_pr)
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0'}
headers['Host']='www.flvxz.com'

def strname(nameStr):
    for i in '\\/:*?"<>&|':
        nameStr=nameStr.replace(i,'')
    return nameStr
def downLoadFile(url,dir):
    # if os.path.isfile(dir):
    #     print '%s >>>>>>>>> already exists ' % dir
    # else:
#    print 'Download:%s-->%s' % (url,dir)
    cmd='wget -c --referer="http://www.yinyuetai.com" "%s" -O "%s"' % (url,dir)
    os.system(cmd)
while True:
 
    id=raw_input('请输入音悦台ID:')
    flvType={'hc':'流畅','hd':'高清','he':'超清',}
    yinyuetaiUrl='http:##v.yinyuetai.com/video/%s'%id
    yinyuetaiUrlCode=base64.b64encode(yinyuetaiUrl)
    url='http://www.flvxz.com/getFlv.php?url=%s'%yinyuetaiUrlCode
    headers['Referer']=url
    opener.addheaders=headers.items()
    # print url
    htmlStr=opener.open(url).read().decode("UTF-8").encode('GB18030','ignore') 
#    print htmlStr
    flvList=re.findall('a rel="noreferrer" href="(.*?)"(.*?)</a>', htmlStr)
#    print flvList
    try:

        for i in flvList:
            print i[0],flvType[re.findall('http://(\w+).yinyuetai.com', i[0])[0]],i[1]
    except Exception, e:
        pass
    l=len(flvList)-1
    try:
        name=flvType[re.findall('http://(\w+).yinyuetai.com', flvList[l][0])[0]]+'_'+strname(flvList[l][1])
    except Exception, e:
        name=strname(flvList[l][1])
    
#    print name
    downLoadFile(flvList[l][0],name)
    