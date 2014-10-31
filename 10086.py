#coding:GBK
__author__ = 'Administrator'

import requests
import shelve
import re

cookie=shelve.open('cookies.dat')
cookies = requests.utils.cookiejar_from_dict(cookie)
# print cookie
# print cookies
# try:
#     jar.load()
# except:
#     r = requests.get('http://foobar.com', cookies=jar)
#     jar.save()

url='http://wap.gd.10086.cn/nwap/login/login.jsps?'
imgCheckCodeUrl='http://wap.gd.10086.cn/nwap/login/wapImageCheckCode/read.jsps?0.46336756048440586'
s=requests.Session()
s.cookies=cookies



# print s.cookies
# print requests.utils.dict_from_cookiejar(s.cookies)
html=s.get('http://wap.gd.10086.cn/nwap/personal/personal/queryFlow.jsps#').content
if 'fr tBlue'  in html:
    print u'读取cookies 登录成功'
# print html
    for i in re.findall('<div>(.*?)<span class="fr tBlue">(.*?)</span>',html):
        print ' '.join(i).decode('UTF-8')


else:
    html=s.get(imgCheckCodeUrl).content
    f=open('checkCode.jpg','wb')
    f.write(html)
    f.close()

    code=raw_input('imageCode:')



    num='15815165532'
    passwd='xxx'
    postdata={
    'backURL':'null',
    'imageCode':code,
    'loginType':'2',
    'mobile':num,
    'needAutoLoginIn2Weeks':'1',
    'password':passwd,
    'portalCode':'null',
    'version':0

    }
    if 'success' in s.post(url,data=postdata).content:
        print u'登录成功'
        cookie.update(requests.utils.dict_from_cookiejar(s.cookies))
        cookie.close()
        html=s.get('http://wap.gd.10086.cn/nwap/personal/personal/queryFlow.jsps#').content
        if 'fr tBlue'  in html:
            # print '读取cookies 登录成功'
        # print html
            for i in re.findall('<div>(.*?)<span class="fr tBlue">(.*?)</span>',html):
                print ' '.join(i).decode('UTF-8')
