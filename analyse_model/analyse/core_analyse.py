# !usr/bin/env python
# -*-coding: utf-8 -*-
__author__ = 'wtq'

import sys
reload(sys)
sys.setdefaultencoding("utf8")
import json
from common_body_parse import common_parse
from analyse_model.util.redis_queue import RedisQueue
from analyse_model.util.conn_mysql import conn_mysql
from analyse_model.analyse.CutWord.operate import content_analyse
from yuqingspider.yuqingspider.common.md5 import md5

redis_queue = RedisQueue('newscontent')
conn = conn_mysql()
mysqlop = conn.cursor()
mysqlop.execute("SET NAMES utf8")
mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
conn.commit()


def analyse():
    """
    read html body from redis and extract text,then analyse it save into mysql
    :return:
    """
    sign = 0
    sqli = "insert into spider_content values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    while True:
        # 实时在redis中取数据
        if not redis_queue.empty():

            sign = 0
            body_raw = redis_queue.get()
            body_split = body_raw.split('@')
            item = json.loads(body_split[0])
            html_body = body_split[1]
            url_md5 = md5(item['url'])
            text = common_parse(html_body)[1]

            analyse_result = content_analyse(text)
            sentiment = analyse_result[0]
            area = analyse_result[1]

            mysqlop.execute(sqli, (url_md5, item['publish_time'], item['spider_name'], item['catch_date'],
                                             item['From'], item['url'], item['title'], item['summary'], item['site_url'],
                                             None, None, None, item['site_name'], text, html_body, area, sentiment))
            conn.commit()
            # print analyse_result[0], analyse_result[1]
            print 'insert one item into mysql'

        else:
            if not sign:
                print 'listening redis queue...'
                print 'queue is empty'
                sign = 1

if __name__ == '__main__':
    analyse()

