#coding:utf-8
import re
import json
import requests
from urlparse import urlparse


def BBS_url_extract(url, keywords):
    res = {'kw': '', 'searchid': ''}
    try:
        r = requests.session()
        a = requests.adapters.HTTPAdapter(max_retries=6)
        b = requests.adapters.HTTPAdapter(max_retries=6)
        r.mount('http://', a)
        r.mount('https://', b)
        print url, keywords
        req = r.get(url)
        codes = req.headers['content-type']
        formhash= re.findall('<input type="hidden" name="formhash" value="([0-9a-z]{8})"', req.text)
        print formhash
        print codes
        print type(keywords)
        if 'gbk' in codes:
            try:
                key = unicode(keywords, 'utf-8').encode('gbk')
                print 'try', key
            except Exception, e:
                print e
                key = keywords.encode('gbk')
                print 'except', key
        else:
            try:
                key = unicode(keywords, 'utf-8').encode('utf-8')
                print 'else try', key
            except:
                key = keywords.encode('gbk')
                print 'else except', key
        data = {'formhash': formhash[0], 'srchtxt':key, 'mod':'forum','searchsubmit':'ture', 'srhfid':'0','srhlocality':'search::forum'}
        print data
        #headers = {"Content-Type": "application/x-www-form-urlencoded", 'Accept-Encoding': ''} 
        headers = {'Accept-Encoding': ''}
        req2 = r.post(url, data = data,  allow_redirects=False,  headers=headers)
        print req2.text
        print req2.headers
        print req2.headers['location']
        for item in req2.headers['location'].split('&'):
            k, v = item.split('=', 1)
            res[k] = v
        print res
    except Exception, e:
        searchid = ''
        print e
    try: 
        return {'keyword': res['kw'], 'searchid' : res['searchid']}
    except:
        pass

if __name__ == '__main__':
    print BBS_url_extract('http://bbs.rqxx.com.cn/search.php', '石油')
