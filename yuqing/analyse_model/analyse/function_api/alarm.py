# !/usr/bin/env python
# -*-coding: utf-8 -*-
__author__ = 'wtq'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from analyse_model.util.transtime import transtime
from analyse_model.util.conn_mysql import conn_mysql

mysql_conn = conn_mysql()
mysqlop = mysql_conn.cursor()
mysqlop.execute("SET NAMES utf8")
mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
mysql_conn.commit()

def alarm(input):
    """
    在item list中的不同热点源所占的条数 源1：20 源2：30 ，，，，，，
    :param input: (itemid list， 回复数阈值)   [[itemid ,…itemid…..], threshold]
    :return: [{itemid:count,itemid:count(每个item在权威站点中出现的次数),,,}, 负倾向占比，回复数超过回复数阈值的itemid]
    """
    item_ids = input['reqData']['item_ids']
    threshold = input['reqData']['threshold']
    response_data = {}
    response_data['sid'] = input['sid']
    response_data['resData'] = {}

    negative_count = 0
    select_item_list = []
    itemid_dict = {}
    static_count = []
    find_sql = "select reply_times, view_times, sentiment, publish_time, type, source_name from t_items where url_md5=%s"

    for item_id in item_ids:
        temp = []
        mysqlop.execute(find_sql, [item_id])
        item = mysqlop.fetchmany(1)[0]
        temp.append(item[3])
        temp.append(item[4])
        temp.append(item[5])
        static_count.append(temp)
        # 判断回复数与浏览数之和是否超过阈值
        if item[0] + item[1] > threshold:
            select_item_list.append(item_id)
            itemid_dict[item_id] = item[3]
        if item[2] == -1:
            negative_count += 1

    # 获取超过阈值的item中发布时间最近的itemid
    latest_time = 1
    latest_id = '123'
    for id_key in itemid_dict:
        item_time = itemid_dict[id_key].strftime('%Y-%m-%d %H:%M:%S')
        if latest_time < transtime(item_time):
            latest_time = transtime(item_time)
            latest_id = id_key
    response_data['resData']['latest_itemid'] = latest_id

    negative_rate = float(negative_count) / len(item_ids)
    response_data['resData']['negative_percent'] = negative_rate
    response_data['resData']['alarm_itemid'] = select_item_list

    day_analyse_dict = {}
    # 每天的数据分析统计结果集合
    for item in static_count:
        publish_time_raw = str(item[0])
        publish_time = publish_time_raw.split(" ")[0]

        if publish_time not in day_analyse_dict:
            day_analyse_dict[publish_time] = {}
            day_analyse_dict[publish_time]['date'] = publish_time
            if item[1] == 'news':
                day_analyse_dict[publish_time]['news_count'] = 1
            else:
                day_analyse_dict[publish_time]['news_count'] = 0
            if item[1] == 'bbs':
                day_analyse_dict[publish_time]['bbs_count'] = 1
            else:
                day_analyse_dict[publish_time]['bbs_count'] = 0
            if item[1] == 'blog':
                day_analyse_dict[publish_time]['blog_count'] = 1
            else:
                day_analyse_dict[publish_time]['blog_count'] = 0
            if item[1] == 'weibo':
                day_analyse_dict[publish_time]['wb_count'] = 1
            else:
                day_analyse_dict[publish_time]['wb_count'] = 0

        else:
            if item[1] == 'news':
                day_analyse_dict[publish_time]['news_count'] += 1
            elif item[1] == 'bbs':
                day_analyse_dict[publish_time]['bbs_count'] += 1
            elif item[1] == 'blog':
                day_analyse_dict[publish_time]['blog_count'] += 1
            elif item[1] == 'weibo':
                day_analyse_dict[publish_time]['wb_count'] += 1

    response_data['resData']['media_count'] = []
    for item_key in day_analyse_dict:
        response_data['resData']['media_count'].append(day_analyse_dict[item_key])

    # 热点源中统计item list 的出现次数
    source_count = {}
    try:
        mysqlop.execute("select cn_name from t_source_used where ishot = 1")
        hot_list = mysqlop.fetchmany(100000)
    except Exception, e:
        print 'select from database error', e

    for s_name in static_count:
        if s_name[2] in hot_list[0]:
            if s_name[2] not in source_count:
                source_count[s_name[2]] = 0
            else:
                source_count[s_name[2]] += 1
    response_data['resData']['items_appear_times'] = []
    for s_key in source_count:
        s_dict = {}
        s_dict['source_name'] = s_key
        s_dict['count'] = source_count[s_key]
        response_data['resData']['items_appear_times'].append(s_dict)
    return response_data


if __name__ == "__main__":
    mysqlop.execute("select title, publish_time, url_md5, source_name, type, url, summary from t_items")
    items = mysqlop.fetchmany(size=1000)
    inputs = {}
    print len(items)
    inputs['sid'] = 5
    inputs['reqData'] = {}
    inputs['reqData']['items'] = []
    inputs['reqData']['depart_id'] = 1
    input_item = []
    for item in items:
        temp_dict = {}
        temp_dict['title'] = item[0]
        temp_dict['publish_time'] = str(item[1])
        temp_dict['itemid'] = item[2]
        input_item.append(item[2])
        temp_dict['source_name'] = item[3]
        temp_dict['type'] = item[4]
        temp_dict['url'] = item[5]
        temp_dict['summary'] = item[6]
        temp_dict['docid'] = 3
        temp_dict['province_id'] = 1
        inputs['reqData']['items'].append(temp_dict)
    # hot_event(inputs)
    # burst_event(inputs)
    topic_input = {}
    topic_input['sid'] = '11111'
    topic_input['reqData'] = {}
    topic_input['reqData']['item_ids'] = input_item
    topic_input['reqData']['threshold'] = 1
    # topic(topic_input)
    alarm(topic_input)
