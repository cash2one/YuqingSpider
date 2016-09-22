# !/usr/bin/env python
# -*-coding: utf-8-*-
__author__ = 'wtq'

import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from conn_mysql import conn_mysql
from searchEngines import SearchEngines
from searchEngines import SearchEngineResultSelectors
from searchName import SearchNames


news = ['baidu', 'sogou', 'youdao', 'qihoo']
blog = ['sogoublog']
weibo = ['weibosearch', 'weibocontent', 'weibohot']

conn = conn_mysql()
mysqlop = conn.cursor()

insert_sql = 'insert into source_site(en_name, ch_name, url, template, type) values (%s,%s,%s,%s,%s)'

for item in SearchEngines:
    en_name = item
    url = SearchEngines[item]
    template = json.dumps(SearchEngineResultSelectors[item])
    if item in SearchNames:
        ch_name = SearchNames[item].encode('utf-8')
    else:
        ch_name = None
    if item in news:
        type = 'news'
    elif item in blog:
        type = 'blog'
    elif item in weibo:
        type = 'weibo'
    else:
        type = 'bbs'

    mysqlop.execute(insert_sql, (en_name, ch_name, url, template, type))

mysqlop.close()
conn.commit()
conn.close()
