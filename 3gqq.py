#coding:GBK
'''
Created on 2014-10-30

@author: llych
'''
import shelve
import requests


loginUrl='http://pt.3g.qq.com/g/s?aid=nLogin'
dbFile='./qq.db'
import re
db=shelve.open(dbFile)
qq=903269993
pwd='xxxx'
#headers={'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'}
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0'}
s=requests.Session()
#def dbOp(k,v):
#    db=shelve.open(dbFile)
#    db[k]=v
#    db.close()
#    
#print db
#
#dbOp('k', 'v')

s.headers.update(headers)
html=s.get(loginUrl).content.decode('UTF-8','ignore')
#print html
postUrl=re.findall('go href="(http://.*?vdata.*?)"',html)[0]
sid=re.findall('name="sid" value="(.*?)"', html)[0]
print postUrl,sid


postData={
         'aid':'nLoginHandle',
'bid':0,
'loginType':1,
'login_url':'http://pt.3g.qq.com/s?aid=nLogin',
'modifySKey':0,
'pwd':pwd,
'qq':qq,
'sid':sid,
'sidtype':1
          
          
          }

html=s.post(postUrl, data=postData).content.decode('UTF-8')
if 'img src' in html:
    imgUrl=re.findall('img src="(.*?)"', html)[0]
    print 'gif -->',imgUrl
    loginPostUrl=re.findall('go href="(http:.*?)"', html)[1]
    hexpwd=re.findall(' name="hexpwd" value="(.*?)"', html)[0]
    print loginPostUrl
    f=open('Verifi.gif','wb')
    f.write(s.get(imgUrl).content)
    f.close()
    verify=raw_input('verify:')
    
    logPostData={
                 
'auto':'0',
'bid':'0',
'bid_code':'qqchatLogin',
#'extend':'http://nvcsz.gtimg.com/728971657/4010706698365962417',
'go_url':'http://ish.z.qq.com/infocenter_v2.jsp?B_UID=258435188&&',
'hexp':'true',
'hexpwd':hexpwd,
'imgType':'gif',
#'loginTitle':'手机腾讯网',
'loginType':'1',
'login_url':'http://pt.3g.qq.com/s?aid=nLogin&from=2&abc=xyz&sid=AVPyxzevdnQk0M2NPa1AQTOi&go_url=http%3A%2F%2Fish.z.qq.com%2Finfocenter_v2.jsp%3FB_UID%3D258435188%26%26',
'modifySKey':'0',  
'q_status':'10',
'qq':qq,
'r':'51348',
#'r_sid':'W2sXFV6YKRYC2jcSUPI0h0lCv0Of1x93KqGwxxI_NMu7UycF71TnbWx8mI2z1q3EGLt2IijXptU3OAMF0ZWnMCLOFPSdkN8AlGnPSRgGfYiyU.BE',
'rip':'119.146.222.92',
'sid':sid,
'u_token':qq,
'verify':verify
                 
                 
                 }
    html=s.post(postUrl, data=logPostData).content.decode('UTF-8')
    print html
