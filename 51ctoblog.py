#!/usr/bin/env python
#coding:gbk
'''
Created on 2013-12-4

@author: llych
'''
import re
import urllib2
import os
import sys

def mkDir(name):
        if not os.path.isdir(name):
            os.mkdir(name)  


def formatStr(nameStr):
    for i in '\\/:*?"<>& | #':
        nameStr=nameStr.replace(i,'')
    return nameStr

def writeHtml(htmlStr,dir):
    if os.path.isfile(dir):
        print '%s >>>>>>>>> already exists ' % dir
    else:
        print 'Download:-->%s' % (dir)
        f=open(dir,'w')
        f.write(htmlStr)
        f.close()
def writeImg(url,dir):
    if os.path.isfile(dir):
        print '%s >>>>>>>>> already exists ' % dir
    else:
        print 'Download:%s-->%s' % (url,dir)
        cmd='wget --referer="http://www.51cto.com" %s -O %s' % (url,dir)
        os.system(cmd)

#列表地址
def blogUrl(url):
    htmlStr=urllib2.urlopen(url).read()
#    print htmlStr
    bUrl=re.findall('<a href="(.*?)" class="fr">文章列表', htmlStr)[0]
    return url+bUrl

def blogList(url):
    return (('http://ahalei.blog.51cto.com/all/4767671',u'算法'),)

def strHtml(url):

#    print url
    htmlStr=urllib2.urlopen(url).read()
#    print htmlStr
    body=re.findall('(<div class="showContent">.*</div><!--正文 end-->)',htmlStr,re.S)[0]

    return body


def allList(url):
    aList=[]
    i=1
    rUrl=re.sub('/all.*','',url)
    
#    print rUrl,'--',purl
    while True:
        try:

#        
            purl=url+'/page/'+str(i)
#            print purl
            htmlStr=urllib2.urlopen(purl).read()
            pList=re.findall('<span class="artList_tit"><a href="(.*?)">(.*?)</a>', htmlStr)
#            print pList[0]
            if pList[0] in aList:
                print 'page-------End'
                break
            else:
                aList.extend(pList)
#            for i in pList:
#                print i[0],i[1]
            i=i+1
        except Exception, e:
            print e
            break

    lenH=len(aList)
    for i in aList:
        yield rUrl+str(i[0]),str('%03d'%lenH)+'_'+i[1]
        lenH=lenH-1
if __name__=='__main__':
    url=sys.argv[1]
    for i in blogList(blogUrl(url)):
        print i
    for i in blogList(blogUrl(url)):
        print i[0],i[1]
        dir=formatStr(i[1])
        print dir
        mkDir(dir)


        for j in allList(i[0]):
            print j[0],j[1]


            body=strHtml(j[0])
##    print body
            img=re.findall('<img.*?src="(.*?)".*?/>',body)
            for k in img:
                print k
                imgName=re.findall('([^/]*\.*$)',k)[0]
                print imgName
                body=body.replace(k,imgName)
                if 'http' in k:
        #            pass
                    writeImg('%s'%(k),dir+'\\'+imgName)
                else:
                    writeImg('%s'%(url+'/'+k),dir+'\\'+imgName)
#                    print 'ERROR---------------------------------------------------'
            dStr='''
    <html>
    
    <head>
    <title>%s</title>
    </head>
    
    <body>
    %s
    </body>
    
    </html>
        ''' % (j[1],body)
            writeHtml(dStr,'%s\%s.html'%(dir,formatStr(j[1])))
