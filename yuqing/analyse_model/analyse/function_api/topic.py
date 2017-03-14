# !/usr/bin/env python
# -*-coding: utf-8 -*-
__author__ = 'wtq'

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from analyse_model.util.transtime import transtime
from analyse_model.util.conn_mysql import conn_mysql
from analyse_model.analyse.accident_event import AccidentEvent

mysql_conn = conn_mysql()
mysqlop = mysql_conn.cursor()
mysqlop.execute("SET NAMES utf8")
mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
mysql_conn.commit()


def topic(input):
    """
    对输入的item进行溯源，媒体关注度，媒体倾向性分析
    :param input:item_id list [item_id,item_id,,,,,item_id,,]
    :return: [source_item_id, count_by_day, count_by_source_type, count_by_sentiment, count_by_source_name, {item_id: source_name, sentiment, media_type}]
    """
    select_item_sql = "select url_md5, publish_time, source_name, type, sentiment, title, summary from t_items where url_md5=%s"
    select_hot_sql = "select cn_name from t_source_used where ishot=1"
    select_depart_sql = "select person_keyword, region_keyword, organization_keyword from t_depart"

    try:
        mysqlop.execute(select_hot_sql)
        hot_source = []
        hot_source_raw = mysqlop.fetchmany(100000)
    except Exception, e:
        print 'select from database error', e

    for hot_item in hot_source_raw:
        # print hot_item[0]
        hot_source.append(hot_item[0])

    response_data = {}
    response_data['sid'] = input['sid']
    response_data['resData'] = {}
    response_data['resData']['sources'] = []
    itemid_list = input['reqData']['item_ids']
    earlyest_time = 7768164660
    # 每条item的相关字段作为一个元素存储在item_list中
    items = []
    media_sentiment_statistics = []
    statistics = []
    class_input = []

    # 存储每个类别的数量，方便来获取数量最高的3类
    length_dict = {}
    select_class = []
    items_dict = {}

    for item_id in itemid_list:
        temp = []
        mysqlop.execute(select_item_sql, [item_id])
        select_item = mysqlop.fetchmany(size=1)[0]
        temp.append(select_item[5])
        temp.append(str(select_item[1]))
        temp.append(select_item[0])
        class_input.append(temp)
        # python datetime 转换为特定格式的string
        item_time = select_item[1].strftime('%Y-%m-%d %H:%M:%S')
        items.append(select_item)
        items_dict[select_item[0]] = select_item

        if earlyest_time > transtime(item_time):
            earlyest_time = transtime(item_time)
            source_item_id = select_item[0]
            source_publish_date = select_item[1]
            source_name = select_item[2]
    #try:
    accident_event = AccidentEvent()
    cluster_result = accident_event.getClustersResult(class_input)
    # except Exception, e:
    #     print 'cluster title error', e

    # 得到报道数量最多的前三类
    for index in range(len(cluster_result)):
        length_dict[index] = len(cluster_result[index])

    length_sort = sorted(length_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    print length_sort
    sign = 0
    for i in length_sort:
        sign += 1
        select_class.append(cluster_result[i[0]])
        if sign > 2:
            break

    # 人物 机构 地域分析
    person = []
    region = []
    organization = []

    mysqlop.execute(select_depart_sql)
    depart_items = mysqlop.fetchmany(100000)

    for d_item in depart_items:
        persons = d_item[0].split(',')
        for p in persons:
            if p not in person:
                person.append(p)
        regions = d_item[1].split(',')
        for r in regions:
            if r not in region:
                region.append(r)
        rogs = d_item[2].split(',')
        for r in rogs:
            if r not in organization:
                organization.append(r)
    # print person
    if len(select_class) > 0:
        for class_item in select_class:
            result_p = ''
            result_r = ''
            result_o = ''
            class_dict = {}
            ids = ""
            id_time_dict = {}
            class_dict['title'] = items_dict[class_item[0]][5]
            # 获得各类中发布时间最早的5篇id
            if len(class_item) >= 5:

                for item_id in class_item:
                    p_time = items_dict[item_id][1]
                    p_time = p_time.strftime('%Y-%m-%d %H:%M:%S')
                    id_time_dict[item_id] = transtime(p_time)

                new_time_dict = sorted(id_time_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
                for i in range(len(new_time_dict)):
                    ids += new_time_dict[i][0] + ","
                    if i == 4:
                        break
            else:
                for i in class_item:
                    ids += i + ","
            class_dict["item_ids"] = ids

            # 每类的人物 机构 地域分析
            for item_id in class_item:
                for p in person:
                    if p in items_dict[item_id][5] or p in items_dict[item_id][6] and p not in result_p:
                        result_p += p + ","
                for r in region:
                    if r in items_dict[item_id][5] or r in items_dict[item_id][6] and r not in result_r:
                        result_r += r + ","
                for o in organization:
                    if o in items_dict[item_id][5] or o in items_dict[item_id][6] and o not in result_o:
                        organization.remove(o)
                        result_o += o + ","
            class_dict['relative_person'] = result_p
            class_dict['relative_region'] = result_r
            class_dict['relative_org'] = result_o
            print result_o
            print result_p
            print result_r
            response_data['resData']['sources'].append(class_dict)
    else:
        response_data['resData']['sources'].append(" ")
    # 热点源的倾向性统计
    sign = 0
    for hot in hot_source:
        sign += 1
        if sign > 6:
            break
        temp_dict = {}
        temp_dict["media_source_name"] = hot
        positive_count = 0
        negative_count = 0
        middle_count = 0
        for item in items:
            if item[2] == hot:
                if item[4] == 1:
                    positive_count += 1
                elif item[4] == -1:
                    negative_count += 1
                elif item[4] == 0:
                    middle_count += 1
        temp_dict["media_positive_count"] = positive_count
        temp_dict['media_negative_count'] = negative_count
        temp_dict['media_neuter_count'] = middle_count
        # print temp_dict
        media_sentiment_statistics.append(temp_dict)
    print len(media_sentiment_statistics)
    response_data['resData']['media_sentiment_statistics'] = media_sentiment_statistics

    day_analyse_dict = {}
    # 该主题每天的数据分析统计结果集合
    for item in items:
        publish_time_raw = str(item[1])
        publish_time = publish_time_raw.split(" ")[0]

        if publish_time not in day_analyse_dict:
            day_analyse_dict[publish_time] = {}
            day_analyse_dict[publish_time]['date'] = publish_time
            day_analyse_dict[publish_time]['date_count'] = 1
            if item[3] == 'news':
                day_analyse_dict[publish_time]['news_count'] = 1
            else:
                day_analyse_dict[publish_time]['news_count'] = 0
            if item[3] == 'bbs':
                day_analyse_dict[publish_time]['bbs_count'] = 1
            else:
                day_analyse_dict[publish_time]['bbs_count'] = 0
            if item[3] == 'blog':
                day_analyse_dict[publish_time]['blog_count'] = 1
            else:
                day_analyse_dict[publish_time]['blog_count'] = 0
            if item[3] == 'weibo':
                day_analyse_dict[publish_time]['wb_count'] = 1
            else:
                day_analyse_dict[publish_time]['wb_count'] = 0
            if item[4] == -1:
                day_analyse_dict[publish_time]['negative_count'] = 1
            else:
                day_analyse_dict[publish_time]['negative_count'] = 0
            if item[4] == 1:
                day_analyse_dict[publish_time]['positive_count'] = 1
            else:
                day_analyse_dict[publish_time]['positive_count'] = 0
            if item[4] == 0:
                day_analyse_dict[publish_time]['neuter_count'] = 1
            else:
                day_analyse_dict[publish_time]['neuter_count'] = 0
        else:
            day_analyse_dict[publish_time]['date_count'] += 1
            if item[3] == 'news':
                day_analyse_dict[publish_time]['news_count'] += 1
            if item[3] == 'bbs':
                day_analyse_dict[publish_time]['bbs_count'] += 1
            if item[3] == 'blog':
                day_analyse_dict[publish_time]['blog_count'] += 1
            if item[3] == 'weibo':
                day_analyse_dict[publish_time]['wb_count'] += 1
            if item[4] == -1:
                day_analyse_dict[publish_time]['negative_count'] += 1
            if item[4] == 1:
                day_analyse_dict[publish_time]['positive_count'] += 1
            if item[4] == 0:
                day_analyse_dict[publish_time]['neuter_count'] += 1

    for key in day_analyse_dict:
        statistics.append(day_analyse_dict[key])
        # print day_analyse_dict[key]

    response_data['resData']['statistics'] = statistics

    return response_data


if __name__ == "__main__":
    mysqlop.execute("select title, publish_time, url_md5, source_name, type, url, summary from t_items")
    items = mysqlop.fetchmany(size=100)
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
        temp_dict['publish_time'] = item[1]
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
    topic(topic_input)
