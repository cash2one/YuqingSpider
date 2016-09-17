#!/usr/local/bin/python2.7
#coding:utf-8
import re
import sys
import json
import requests

from scrapy.selector import Selector
COOKIE_PATH = '/root/seCrawler/seCrawler/config/COOKIE.FILE'

def extract_weibo_comment(uid, cookies):
    url = 'http://weibo.com/u/%s' % (uid)
    result = ''
    try:
        res = requests.get(url, cookies = cookies, timeout=10).text
        pageid = re.findall('\$CONFIG\[page_id\]=(.*);', res.replace('\'', ''));
        detailurl = 'http://weibo.com/p/%s/info?mod=pedit_more' % pageid[0]
        res2 = requests.get(detailurl, cookies = cookies, timeout = 10).text
        #print detailurl
        #print res2 
        blocks = Selector(text = res2).xpath('//script')
        INFO = ''
        NUM = ''
        for block in blocks:
            block= block.extract().encode('utf8').replace(r'\"', r'"').replace(r'\/', r'/')
            num = Selector(text=block[16:-10]).xpath('.//strong/text()').extract()
            info =  Selector(text=block[16:-10]).xpath('.//span[@class="pt_detail"]//text()').extract()
            if info:
                INFO = info
            if num:
                NUM = num
        watch = NUM[0]
        fans = NUM[1]
        weibo = NUM[2]
        nick = INFO[0].strip()
        location = INFO[1].strip()
        sex = INFO[2].strip()
        print json.dumps({'uid': uid, 'watch':watch, 'fans':fans, 'weibo':weibo, 'nick':nick, 'location':location, 'sex':sex}) 
    except Exception, e:
        #print e
        #print json.dumps({'error':e})
        detailurl = 'http://weibo.com/u/%s' % uid
        res2 = requests.get(detailurl, cookies = cookies, timeout = 10).text
        #print detailurl
        #print res2 
        blocks = Selector(text = res2).xpath('//script')
        INFO = ''
        NUM = ''
        for block in blocks:
            block= block.extract().encode('utf8').replace(r'\"', r'"').replace(r'\/', r'/')
            num = Selector(text=block[16:-10]).xpath('.//strong/text()').extract()
            if num:
                NUM = num
        watch = NUM[0]
        fans = NUM[1]
        weibo = NUM[2]
        print json.dumps({'uid': uid, 'watch':watch, 'fans':fans, 'weibo':weibo}) 


if __name__ == '__main__':
    cookies = json.loads(open(COOKIE_PATH).read())
    extract_weibo_comment(sys.argv[1], cookies)
