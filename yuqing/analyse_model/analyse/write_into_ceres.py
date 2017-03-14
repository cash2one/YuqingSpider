# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import ast
import time
import redis
import threading
from gevent import monkey
from analyse_model.util.conn_mysql import conn_mysql

monkey.patch_all()
conn = conn_mysql()
mysqlop = conn.cursor()
mysqlop.execute("SET NAMES utf8")
mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
conn.commit()

sqli = "insert into t_items values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


def callback():
    r = redis.client.StrictRedis()
    sub = r.pubsub()
    sub.subscribe('complete_items_channel')

    for m in sub.listen():
        try:
            if len(str(m['data'])) > 5:
                # string item 转换成 dict
                item = ast.literal_eval(str(m['data']))
                # item为字典类型，可将item进入到ceres中
        except Exception, e:
            print 'error in insert into database', e


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
