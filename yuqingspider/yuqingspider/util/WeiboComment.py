#!/usr/local/bin/python2.7
#coding:utf8
import re
import sys
import json
import requests

from scrapy.selector import Selector

COOKIE_PATH = '/root/seCrawler/seCrawler/config/COOKIE.FILE'


def extract_weibo_comment(mid, cookies, size=3):
    url = 'http://weibo.com/aj/v6/comment/small?ajwvr=6&act=list&mid=%s' % (mid)
    #print 'Get comments URL: %s\n' % url
    result = ''
    try:
        res = requests.get(url, cookies=cookies, timeout=10).text
        html = json.loads(res)['data']['html']
        #print html
        blocks = Selector(text=html).xpath('//div[@class="list_li S_line1 clearfix"]')
        for block in blocks[:size]:
            content = block.xpath('string(.//div[@class="WB_text"])').extract()
            result += '@'+''.join(content).strip() + '\n'
    except Exception, e:
        #print e
        result= '' 
    return json.dumps({'comment':result})


if __name__ == '__main__':
    cookies = json.loads(open(COOKIE_PATH).read())
    #print extract_weibo_comment('3905150441281291', '5542078300', cookies)
    #print extract_weibo_comment('3905150441281291', cookies)
    print extract_weibo_comment(sys.argv[1], cookies)
