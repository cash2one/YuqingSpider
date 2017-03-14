# !/usr/bin/env python2.7
# -*-coding: utf-8 -*-
__author__ = 'wtq'

import os
import sys
reload(sys)
import redis
import chardet
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.setdefaultencoding("utf8")

import ast
import time
import json
import logging
from datetime import datetime
from common_body_parse import common_parse
from analyse_model.util.redis_queue import RedisQueue
from analyse_model.util.conn_mysql import conn_mysql
from analyse_model.analyse.CutWord.operate import content_analyse
from analyse_model.util.md5 import md5
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

current_path = os.path.dirname(__file__)
logging.basicConfig(filename=current_path + '/logger.log', level=logging.ERROR)

item_queue_raw = RedisQueue('items')
coml_queue = RedisQueue('complete_items')
re = redis.Redis(host='127.0.0.1', port=6379)

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
    depart_list = get_depart()

    sqli = "insert into t_items values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    while True:
        # 实时在redis中取数据
        # 无发布时间的news不存入mysql
        try:
            if not item_queue_raw.empty():
                body_raw = item_queue_raw.get()
                item = json.loads(body_raw)
                # item = ast.literal_eval(body_raw)
                # t_depart 表有新内容时重新读取t_depart表
                if 'has_new_depart' in item:
                    depart_list = get_depart()
                # 否则对传过来的字段进行处理
                else:
                    if item["From"] != "weibo":
                        html_body = item['html_body']
                        store_html_body = item['html_body']
                        url_md5 = md5(item['url'])
                    else:
                        # weibo的md5由正文生成
                        url_md5 = md5(item["text"])

                    item['url_md5'] = url_md5

                    # weibo的item或者具有正文模板的item中会包含text字段
                    if 'text' in item:
                        text = item['text']
                    else:
                        content = common_parse(html_body)
                        text = content[1]

                    if not isinstance(text, unicode):
                        code_type = chardet.detect(text)['encoding']
                        print 'not unicode text', code_type
                        if code_type == 'GB2312':
                            code_type = 'gbk'
                        try:
                            text = text.decode(code_type).encode('utf-8')
                        except Exception, e:
                            print 'encode error', e
                    else:
                        text = text.encode('utf-8')
                        # print 'is unicode text'

                    analyse_result = content_analyse(text)
                    sentiment = analyse_result[0]

                    if item['From'] == 'bbs':
                        author = item['author']
                        replay_times = int(item['replay_times'])
                        view_times = int(item['view_times'])
                    elif item['From'] == 'weibo':
                        author = item['author']
                        replay_times = int(item['comments'])
                        view_times = int(item['attitude']) + int(item['repost'])
                        item['site_name'] = item['name']
                        item['source_name'] = item['name']
                        item['summary'] = ""
                    else:
                        author = None
                        replay_times = 0
                        view_times = 0

                    # 对html_body编码类型进行判断，不是unicode的进行转换
                    if item["From"] != 'weibo':
                        if not isinstance(store_html_body, unicode):
                            code_type = chardet.detect(store_html_body)['encoding']

                            if code_type == 'GB2312':
                                code_type = 'gbk'
                            try:
                                html_body = store_html_body.decode(code_type).encode('utf-8')
                            except Exception, e:
                                html_body = store_html_body
                        else:
                            html_body = store_html_body.encode('utf-8')
                    # weibo的html_body为空
                    else:
                        html_body = ""

                    # item html_body text再入另一个队列 供其他逻辑模块使用或者存到打数据平台
                    item['text'] = text
                    item['html_body'] = html_body
                    item['author'] = author
                    item['replay_times'] = replay_times
                    item['view_times'] = view_times
                    item['sentiment'] = sentiment
                    if 'url' not in item.keys():
                        item['url'] = ""
                    # 根据text，title与t_depart 中的key_word 匹配得到 depart_id area_id province_id
                    if item["From"] != "weibo":
                        match_result = match_item(item['title'], item['summary'], text, depart_list)
                    else:
                        match_result = match_item(item['title'], "", text, depart_list)

                    item['depart_list'] = match_result[0]
                    item['area_list'] = match_result[1]
                    item['province_list'] = match_result[2]
                    print 'one item analysed'
                    re.publish('complete_items_channel_new', item)

            else:
                time.sleep(5)
                print 'listening redis queue...'
                print 'queue is empty'

        except Exception, e:
            logging.error(e)
            print 'analyse error', e


def match_item(title, summary, text, depart_list):
    """
    对于每个item由 depart表进行匹配得到该item对应的 area_id list, depart_id list, province_id list
    :param title:
    :param text:
    :return:
    """
    depart_id_list = []
    area_id_list = []
    province_id_list = []
    for depart_item in depart_list:
        sign = 0
        for keyword in depart_item[3]:
            if keyword in title or keyword in text or keyword in summary:
                sign = 1
                break
        if sign:
            depart_id_list.append(depart_item[0])
            area_id_list.append(depart_item[1])
            province_id_list.append(depart_item[2])

    result = [depart_id_list, area_id_list, province_id_list]
    return result


def get_depart():
    """
    :return:
    """
    depart_list = []
    get_depart_sql = "select id, area_id, province_id, person_keyword, region_keyword, organization_keyword from t_depart"
    mysqlop.execute(get_depart_sql)
    depart_items = mysqlop.fetchmany(size=100000)
    for d_item in depart_items:
        temp_item = []
        sub_word = []
        for i in range(3):
            temp_item.append(int(d_item[i]))
        for j in range(3, 6):
            if d_item[j]:
                sub_word.extend(d_item[j].split(","))

        for i in sub_word:
            print i
        print "one item......"

        temp_item.append(sub_word)
        # print temp_item
        depart_list.append(temp_item)
    return depart_list


if __name__ == '__main__':
    analyse()
    # get_depart()


