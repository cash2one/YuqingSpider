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


news = ['baidu', 'sogou', 'youdao', 'qihoo', 'china_net', 'guangming_net', 'xinhua_net', 'people_net', 'baidu_class']
blog = ['sogoublog']
weibo = ['weibosearch', 'weibocontent', 'weibohot']

conn = conn_mysql()
mysqlop = conn.cursor()
mysqlop.execute("SET NAMES utf8")
mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
conn.commit()


def insert_template_into_mysql():
    insert_sql = 'insert into t_source_used(cn_name, url, template, type) values (%s,%s,%s,%s)'

    # for item in SearchEngines:
    item = 'huanqiu_net'
    url = SearchEngines[item]
    template = json.dumps(SearchEngineResultSelectors[item])

    # if item in SearchNames:
    #     cn_name = SearchNames[item].encode('utf-8')
    # else:
    #     cn_name = None

    cn_name = "环球网"
    type = "media"
    # if item in news:
    #     type = 'news'
    # elif item in blog:
    #     type = 'blog'
    # elif item in weibo:
    #     type = 'weibo'
    # else:
    #     type = 'bbs'

    mysqlop.execute(insert_sql, (cn_name, url, template, type))

    mysqlop.close()
    conn.commit()
    conn.close()


def change_source_template():
    mysqlop.execute("select cn_name, template from t_source_used where type='bbs'")
    update_sql = "update t_source_used set template=%s where cn_name=%s"
    sources = mysqlop.fetchmany(size=100)

    for source in sources:
        cn_name = source[0]
        template = json.loads(source[1])
        if 'text' in template['title']:
            new_title = template['title'].split('/text')[0]
            template['title'] = new_title
        if 'text' in template['abstract']:
            new_abstract = template['abstract'].split('/text')[0]
            template['abstract'] = new_abstract
            template_new = json.dumps(template)
            mysqlop.execute(update_sql, (template_new, cn_name))
            conn.commit()

if __name__ == "__main__":
    # change_source_template()
    insert_template_into_mysql()
