#coding:utf-8
import re
import json
import logging
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
        logging.info(url)
        req = r.get(url)
        codes = req.headers['content-type']
        formhash = re.findall('<input type="hidden" name="formhash" value="([0-9a-z]{8})"', req.text)

        if 'gbk' in codes:
            try:
                key = unicode(keywords, 'utf-8').encode('gbk')
                print 'try', key
            except Exception, e:
                logging.info('bbs_extract_error gbk')
                logging.info(e)
                key = keywords.encode('gbk')
                print 'except', key
        else:
            try:
                key = unicode(keywords, 'utf-8').encode('utf-8')
                print 'else try', key
            except Exception, e:
                logging.info("not gbk bbs_extract_error")
                logging.info(e)
                key = keywords.encode('gbk')
                print 'else except', key
        data = {'formhash': formhash[0], 'srchtxt':key, 'mod':'forum','searchsubmit':'ture', 'srhfid':'0','srhlocality':'search::forum'}

        #headers = {"Content-Type": "application/x-www-form-urlencoded", 'Accept-Encoding': ''} 
        headers = {'Accept-Encoding': ''}
        req2 = r.post(url, data=data,  allow_redirects=False,  headers=headers)

        for item in req2.headers['location'].split('&'):
            k, v = item.split('=', 1)
            res[k] = v
    except Exception, e:
        logging.info('bbs_extract_error_all')
        logging.info(e)
        searchid = ''
        print e
    try: 
        return {'keyword': res['kw'], 'searchid': res['searchid']}
    except Exception, e:
        logging.info("bbs extract return error")
        logging.info(e)
        pass

if __name__ == '__main__':
    print BBS_url_extract('http://bbs.rqxx.com.cn/search.php', '石油')
