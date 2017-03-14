# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import ast
from datetime import datetime
import time
import redis
import threading
from gevent import monkey
monkey.patch_all()
from analyse_model.util.conn_mysql import conn_mysql
conn = conn_mysql()
mysqlop = conn.cursor()
mysqlop.execute("SET NAMES utf8")
mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
conn.commit()
re_new = redis.Redis(host='127.0.0.1', port=6379)

sqli_class = "insert into t_items values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sqli = "insert into t_items values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_count = "select count(*) from t_items where url_md5=%s"


def callback():
    r = redis.client.StrictRedis()
    sub = r.pubsub()
    sub.subscribe('complete_items_channel_new')
    global conn, mysqlop

    for m in sub.listen():
        try:
            if len(str(m['data'])) > 5:
                # string item 转换成 dict
                item = ast.literal_eval(str(m['data']))
                print item['publish_time']
                try:
                    publish_time = datetime.fromtimestamp(int(item['publish_time']))
                except Exception, e:
                    publish_time = datetime.fromtimestamp(int(time.time()))

                try:
                    crawl_time = datetime.fromtimestamp(int(item['catch_date']))
                except Exception, e:
                    crawl_time = datetime.fromtimestamp(int(time.time()))

                # item['match_result'］包含depart_id list, area_id list, province id list
                print item['depart_list']
                print item['area_list']
                print item['province_list']

                province_id_list = ""
                if len(item['province_list']) > 0:
                    for p_id in item['province_list']:
                        province_id_list += str(p_id) + ","
                try:
                    if 'item_class' in item.keys():
                        mysqlop.execute(sqli_class,
                                        (item['url_md5'], publish_time, item['source_name'].encode('utf-8'), crawl_time,
                                         item['From'], item['url'], item['title'], item['summary'],
                                         item['author'], item['replay_times'], item['view_times'], item['site_name'],
                                         item['text'], item['html_body'], item['sentiment'], item['key_word'], province_id_list, item['item_class']))
                    else:
                        mysqlop.execute(sqli,
                                        (item['url_md5'], publish_time, item['source_name'].encode('utf-8'), crawl_time,
                                         item['From'], item['url'], item['title'], item['summary'],
                                         item['author'], item['replay_times'], item['view_times'], item['site_name'],
                                         item['text'], item['html_body'], item['sentiment'], item['key_word'], province_id_list, item["source_name"]))
                    conn.commit()
                    re_new.publish("complete_items_channel", item)

                except Exception, e:
                    # 实现微薄论坛的评论浏览数的更新操作
                    print "error in insert mysql", e
                    update_sql = 'update t_items set reply_times=%s,view_times=%s where url_md5=%s'
                    mysqlop.execute(update_sql, [item['replay_times'], item['view_times'], item['url_md5']])
                    conn.commit()

        except Exception, e:
            print 'error in insert into database', e
            conn = conn_mysql()
            mysqlop = conn.cursor()
            mysqlop.execute("SET NAMES utf8")
            mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
            mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
            conn.commit()


def yuqing_rush(n):
    for x in range(n):
        t = threading.Thread(target=callback)
        t.setDaemon(True)
        t.start()


def main():
    yuqing_rush(1)
    while True:
        print 'Waiting'
        time.sleep(3)


if __name__ == '__main__':
    main()


