# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wtq'

import MySQLdb

from config import MYSQL_HOST, MYSQL_PASSWD
from config import MYSQL_PORT, MYSQL_PASSWD, MYSQL_HOST, MYSQL_USER, SPIDER_DB


def conn_mysql(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=SPIDER_DB, charset="utf8"):
    conn = MySQLdb.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWD,
        db=SPIDER_DB
    )
    conn.set_character_set('utf8')
    return conn
