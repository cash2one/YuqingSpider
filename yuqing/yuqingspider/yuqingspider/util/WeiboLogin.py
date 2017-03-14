# coding=utf8

import cookielib
import requests
import urllib2
import random
import json
import time
import re

import WeiboEncode  #微博用户名和密码加密模块
import WeiboSearch  #微博登陆请求的POSTS相关数据获取
import seCrawler.settings as conf

class WeiboLogin:

    def __init__(self, user, pwd, cookieFile, enableProxy = False):
        "初始化WeiboLogin，enableProxy表示是否使用代理服务器，默认关闭"

        print "Initializing WeiboLogin..."
        self.userName = user
        self.passWord = pwd
        self.enableProxy = enableProxy
        self.cookieFile = conf.COOKIE_PATH
        print "UserName:", user
        print "Password:", pwd

        self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
        self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

    def GetServerTime(self):
        "Get server time and nonce, which are used to encode the password"

        print "Getting server time and nonce..."
        serverData = urllib2.urlopen(self.serverUrl).read() #得到网页内容
        print serverData

        try:
	    serverTime, nonce, pubkey, rsakv = WeiboSearch.sServerData(serverData) #解析得到serverTime，nonce等
	    return serverTime, nonce, pubkey, rsakv
        except:
	    print 'Get server time & nonce error!'
	    return None


    def EnableCookie(self, enableProxy):
        "Enable cookie & proxy (if needed)."

        cookiejar = cookielib.LWPCookieJar()#建立cookie
        cookie_support = urllib2.HTTPCookieProcessor(cookiejar)

        if enableProxy:
            proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})#使用代理
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
            print "Proxy enabled"
        else:
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

        urllib2.install_opener(opener)#构建cookie对应的opener
        return cookiejar

    def Login(self):
        "登陆程序"

        cookiejar = self.EnableCookie(self.enableProxy) #cookie或代理服务器配置

        serverTime, nonce, pubkey, rsakv = self.GetServerTime() #登陆的第一步
        postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)   #加密用户和密码
        print "Post data length:\n", len(postData)

        req = urllib2.Request(self.loginUrl, postData, self.postHeader)
        print "Posting request..."
        result = urllib2.urlopen(req)   #登陆的第二步——解析新浪微博的登录过程中3
        text = result.read()
        try:
            loginUrl = WeiboSearch.sRedirectData(text)  #解析重定位结果
            urllib2.urlopen(loginUrl)
        except:
            print 'Login error!'
            return False
        cookies = {}
        for cookie in cookiejar:
            cookies[cookie.name] = cookie.value
        print cookies
        if TestCookie(cookies):
            open(self.cookieFile, 'w').write(json.dumps(cookies))
            #cookiejar.save(self.cookieFile)
            print 'Login sucess!'
            return True
        else:
            return False

def GenCookie():
    userlist = open(conf.USER_PATH).read().split('\n')
    user = random.choice(userlist).strip()
    #user = userlist[0]
    print 'GenCookie now', user
    username, password = user.split(' ')
    weiboLogin = WeiboLogin(username, password, conf.COOKIE_PATH)
    res = weiboLogin.Login()
    if not res:
        GenCookie()

def TestCookie(cookies):
    r = requests.get('http://s.weibo.com/', cookies = cookies)
    if '$CONFIG[\'islogin\'] = \'1\';' in r.text and 'pincode' not in r.text:
        #print r.text
        return True
    else:
        return False
 
if __name__ == '__main__':
    GenCookie()
    cookies = json.loads(open(conf.COOKIE_PATH).read())
    #print cookies
    print TestCookie(cookies)
    #weiboLogin = WeiboLogin('1091fei@sina.com', '1091fei', 'COOKIE.FILE') #邮箱（账号）、密码
