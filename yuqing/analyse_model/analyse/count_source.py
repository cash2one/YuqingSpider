# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wtq'


import time
from datetime import datetime
from analyse_model.util.conn_mysql import conn_mysql
from analyse_model.util.transtime import transtime


def count_source(bbsday, otherday):
    """
    在items中统计每个源的爬取数量并插入到 source表中
    :return:
    """
    conn = conn_mysql()
    mysqlop = conn.cursor()
    mysqlop.execute("SET NAMES utf8")
    mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
    mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
    conn.commit()

    select_source = "select cn_name, type from t_source_used"
    count_sql = "select count(*) from t_items where source_name=%s"
    update_count = "update t_source_used set crawl_num=%s,crawl_time=%s where cn_name=%s"
    update_status = "update t_source_used set status=%s where cn_name=%s"
    get_latest_time = "select latest_time from source_latest_time where source_name=%s"

    mysqlop.execute(select_source)
    sources = []
    sources_type = []
    sources_raw = mysqlop.fetchmany(size=10000000)

    for item in sources_raw:
        sources.append(item[0])
        sources_type.append(item[1])

    # 统计每个源的爬取量更新到source表中

    for source in sources:
        mysqlop.execute(count_sql, [source])
        count = mysqlop.fetchmany(1)[0]
        print source, count[0]
        source_count_time = datetime.fromtimestamp(int(time.time()))
        mysqlop.execute(update_count, [count[0], source_count_time, source])
        conn.commit()

    current_timestamp = int(time.time())
    # 获取每个源的所爬取信息的最新时间，如果与当前日期之差大于deadline就在source表中该源status标记-1
    for i in range(len(sources)):
        mysqlop.execute(get_latest_time, [sources[i]])
        latest_time = mysqlop.fetchmany(1)
        if len(latest_time) > 0:
            # bbs 时间间隔设为5天
            if sources_type[i] == 'bbs':
                if current_timestamp - transtime(str(latest_time[0][0])) > bbsday*86400:
                    mysqlop.execute(update_status, [-1, sources[i]])
            # 其他类型的时间间隔设为2天
            else:
                if current_timestamp - transtime(str(latest_time[0][0])) > otherday*86400:
                    mysqlop.execute(update_status, [-1, sources[i]])
        else:
            mysqlop.execute(update_status, [-1, sources[i]])
            conn.commit()

    mysqlop.close()
    conn.close()
    # mysqlop.close()
    time.sleep(5)

if __name__ == "__main__":
    count_source(5, 2)
