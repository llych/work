#!/usr/bin/env python
#coding:gbk
'''
Created on 2013-12-5

@author: llych
'''

import urllib2
import re
import os
import sys
import time
import logging

count=0
Html='''
<html>

<head>
<title>%s</title>
</head>

<body>
%s
</body>

</html>
'''
def func_time(func):
    def _wrapper(*args,**kwargs):
        start = time.time()
        func(*args,**kwargs)
        logstr=func.__name__+' run:'+str(time.time()-start)
        print logstr
        log.info(str(logstr))
    return _wrapper
def msgLog(logfile):

    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger

def mkDir(name):
        if not os.path.isdir(name):
            os.mkdir(name)  

def formatStr(nameStr):
    for i in '\\/:*?"<>& | #.':
        nameStr=nameStr.replace(i,'')
    return nameStr

def writeHtml(htmlStr,dir):
    if os.path.isfile(dir):
        strlog='%s >>>>>>>>> already exists ' % dir
        print strlog
        log.warn(strlog)
    else:
        strlog= '[%s]Download:-->%s' % (count,dir)
        print strlog
        log.info(strlog)
        f=open(dir,'w')
        f.write(htmlStr)
        f.close()
def writeImg(url,dir):
    if os.path.isfile(dir):
        strlog='%s >>>>>>>>> already exists ' % dir
        print strlog
        log.warn(strlog)
    else:
        strlog= '[%s]Download:%s-->%s' % (count,url,dir)
        print strlog
        log.info(strlog)
        cmd='wget -t 3 %s -O %s' % (url,dir)
        # cmd='wget --referer="http://www.51cto.com" %s -O %s' % (url,dir)
        os.system(cmd)        
#def writeImg(url,dir):
#    if os.path.isfile(dir):
#        strlog='%s >>>>>>>>> already exists ' % dir
#        print strlog
#        log.warn(strlog)
#    else:
#        strlog= '[%s]Download:%s-->%s' % (count,url,dir)
#        print strlog
#        log.info(strlog)
#        try:
#            
#
#            img=urllib2.urlopen(url).read()
#            f=open(dir,'wb')
#            f.write(img)
#            f.close()
#
#        except Exception, e:
#            strlog= '[ERROR%s]Download:%s ERROR---------------%s' % (count,url,e)
#            print strlog
#            log.error(strlog)
@func_time
def strHtml(name,title,url):
    htmlStr=urllib2.urlopen(url).read().decode("UTF-8").encode('GB18030','ignore')
#    print htmlStr
    r=re.findall('(<div id="cnblogs_post_body">.*?<div class="clear"></div>)', htmlStr, re.S)

#    print r[0]
    img=re.findall('<img.*?src="(.*?)".*?>',r[0])
#    print img
    for i in img:
        imgName=re.sub('.*/', '', i)
        if 'http' in i:
            writeImg(i,'%s\%s'%(name,imgName))
        else:
            log.error( "http img Error----------------------------------------------")
#            write
        
        
        r[0]=r[0].replace(i,imgName)
    writeHtml(Html%(title,r[0]),'%s\%s.html'%(name,formatStr(title)))
def blogUrl(url):
    htmlStr=urllib2.urlopen(url).read().decode("UTF-8").encode('GB18030','ignore')
#    print htmlStr
    r=re.findall('<a id="ctl\d+_CatList_LinkList_0_Link_\d+" href="(.*?)">(.*?)\(\d+\)</a>', htmlStr)
#    print r
    print '分类总数:%s'%len(r)
    for i in r:
#        print i[0],i[1]
        dir=formatStr(i[1])
        mkDir(dir)
        analysisHtml(dir,i[0])

def analysisHtml(name,url):
    global count
#    fcount=0
    htmlStr=urllib2.urlopen(url).read().decode("UTF-8").encode('GB18030','ignore')
#    print htmlStr    
    r=re.findall('<a id="CategoryEntryList1_EntryStoryList_Entries_TitleUrl_\d+".*?href="(.*?)">(.*?)</a>', htmlStr)

    flen=len(r)
    print '%s--此分类有文章数:%s'%(name,flen)
    for i in r:
        
        print i[0],i[1]
        count=count+1
        strHtml(name,'%03d_%s'%(flen,i[1]),i[0])
        flen=flen-1
if __name__ == '__main__':
    user=sys.argv[1]
#    user='jackei'
    url='http://www.cnblogs.com/%s/mvc/blog/sidecolumn.aspx' % (user)
    log=msgLog('%s.log'%(user))
    print url
    blogUrl(url)
    print '总文章数量:%s'%count


#    strHtml('aa','---------','http://www.cnblogs.com/jackei/archive/2006/11/20/565527.html')
