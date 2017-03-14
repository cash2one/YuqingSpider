# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import os
import sys
reload(sys)
import jieba
sys.setdefaultencoding("utf8")
import time
import chardet
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from analyse_model.analyse.accident_event import AccidentEvent
from analyse_model.util.conn_mysql import conn_mysql

mysql_conn = conn_mysql()
mysqlop = mysql_conn.cursor()
mysqlop.execute("SET NAMES utf8")
mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
mysql_conn.commit()


def burst_event(input):
    """
    计算该条depart_id相关的各个item最近一段时间媒体报道速率情况
    :param input: 同hot_event中的input  你们可以根据每个元素中的event_rate大小决定其对应的keyword是否做为突发事件
    :return: {depart_id :[[event_rate(次数／每小时), [keyword ,keyword这段时间出现的次数]],,,,,,[],,,,[],,,]}
    """
    input_list = []
    response_data = {}
    select_item_sql = "select title, publish_time from t_items where url_md5=%s"

    response_data['sid'] = input['sid']
    response_data['resData'] = {}
    response_data['resData']['depart_id'] = input['reqData']['depart_id']
    response_data['resData']['burst_events'] = []

    for item in input['reqData']['items']:
        temp = []
        mysqlop.execute(select_item_sql, [item['itemid']])
        select_item = mysqlop.fetchmany(size=1)[0]
        temp.append(unicode(select_item[0], 'utf-8'))
        temp.append(select_item[1])
        temp.append(item['itemid'])
        input_list.append(temp)

    try:
        accident_event = AccidentEvent()
        accident_event.getClustersResult(input_list)
        event_result = accident_event.accidentEventDetection()
    except Exception, e:
        print 'error in cluster', e

    for i in event_result:
        if i[1] <= 10:
            temp_dict = {}
            temp_dict['title'] = i[2]
            print i[2]
            temp_dict['keywords'] = []
            for j in i[0]:
                sub_dict = {}
                sub_dict['keyword'] = j[0]
                print 'keyword', j[0]
                sub_dict['times_minute'] = i[1]
                sub_dict['times_total'] = j[1]
                temp_dict['keywords'].append(sub_dict)
            print 'temp_dict_keyword', temp_dict
            response_data['resData']['burst_events'].append(temp_dict)

    # code = chardet.detect(response_data)["encoding"]
    # print code
    # return response_data


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
    burst_event(inputs)
    # ret = sorted(ret_list, key=lambda ret: ret[1])

