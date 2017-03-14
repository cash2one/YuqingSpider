#!/usr/local/bin/python2.7
#coding:utf-8
import re
import sys
import json
import requests

from scrapy.selector import Selector

COOKIE_PATH = '/root/seCrawler/seCrawler/config/COOKIE.FILE'

def extract_weibo_uid(url, onick = '', cookies=''):
    if onick:
        url = 'http://weibo.com/%s?is_all=1' % onick
    try:
    #    print url
        html = requests.get(url, cookies = cookies, timeout=10).text
    #    print html
        oid = re.findall('CONFIG\[\'oid\'\]=\'(.*)\';', html)[0]
    #    print oid
    except Exception, e:
        print e
        oid = '0'
    return json.dumps({'uid':oid})


if __name__ == '__main__':
    cookies = json.loads(open(COOKIE_PATH).read())
    #print extract_weibo_comment('3905150441281291', '5542078300', cookies)
    #print extract_weibo_comment('3905150441281291', cookies)
    print extract_weibo_uid(sys.argv[1], sys.argv[2], cookies)
