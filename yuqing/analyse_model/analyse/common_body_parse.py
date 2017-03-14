# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wtq'
import os
import re
import sys
import chardet
import logging
import json
reload(sys)
sys.setdefaultencoding("utf-8")
import redis
from analyse_model.util.redis_queue import RedisQueue
from readability import Document
from analyse_model.util.conn_mysql import conn_mysql

content_queue = RedisQueue('newscontent')
current_path = os.path.dirname(__file__)
logging.basicConfig(filename=current_path + '/loggernew.log')

def filter_tags(htmlstr):
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s


def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }
    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string, s)


def common_parse(html_body):
    """
    common parse the html body then extract title and article
    :param html_body:
    :return:list[title, article]
    """
    # html_raw = urllib2.urlopen(url)
    # html_body = html_raw.read()
    try:
        ori_article = Document(html_body).summary()
        article = filter_tags(ori_article)
        # article = unicode(article, 'utf-8')
    except Exception, e:
        article = 'None'

    try:
        title = Document(html_body).short_title()
    except Exception, e:
        title = 'None'

    return [title, article.strip()]


def batch_extract():
    body_raw = content_queue.get()
    body_split = body_raw.split('@')
    print body_split[0]
    json_item = json.loads(body_split[1])
    for item in json_item:
        print item, json_item[item]
    print common_parse(body_split[2])[1]


def batch_extract_old():
    """
    read html body from redis then extract title and body save into mysql
    :return:
    """
    r = redis.StrictRedis()
    conn = conn_mysql()
    mysqlop = conn.cursor()
    update_sql = 'update spider_content set text=%s where url_md5=%s'
    # select_sql = 'select url_md5 from spider_content where type=1'
    mysqlop.execute("select url_md5, url from spider_content where text is null and type='1'")

    urls = mysqlop.fetchmany(size=100000)
    for url in urls:
        try:
            url_md5 = url[0]
            # get html_body from redis
            html_body = r.get(url_md5)
            if html_body:
                print url_md5
                extract_content = common_parse(html_body)

                # 正文存入到 redis,mysql
                r.set(url_md5, extract_content[1])
                mysqlop.execute(update_sql, (extract_content[1].encode('utf-8'), url_md5))
            # 去数据库中查找url直接下载html_body
        except Exception, e:
            print 'common parse error', e

    mysqlop.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    batch_extract()
    # batch_extract_old()

