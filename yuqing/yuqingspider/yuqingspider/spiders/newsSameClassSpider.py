# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wtq'
import os
import sys

reload(sys)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.setdefaultencoding('utf-8')
import time
from datetime import datetime
import json
import chardet
import random
import logging
from ..util.md5 import md5
from scrapy import Request
from scrapy.spiders import Spider
from ..common.config import CRAWLER_TIME_SIGN
from ..common.config import SIGN_TIME_STAMP
from ..common.conn_mysql import conn_mysql
from ..common.searResultPages import searResultPages
from scrapy.selector import Selector
from ..util.transtime import transtime
from ..util.redis_queue import RedisQueue

# 'newsItem':[Item, Item, Item, Item]
content_queue = RedisQueue('items')  # 'newsContent':[{url:}]

mysql_conn = conn_mysql()


class newsSameClassSpider(Spider):
    name = 'newsSameClassSpider'
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None
    item_json = None

    def __init__(self, pages=30, *args, **kwargs):

        super(newsSameClassSpider, self).__init__(*args, **kwargs)
        # self.item = BaseItem()
        self.item = dict()
        # store the next latest time, crawl the news when the publish time bigger then it
        self.latest_time = dict()

        mysqlop = mysql_conn.cursor()
        mysqlop.execute("SET NAMES utf8")
        mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
        mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
        mysql_conn.commit()

        # get key words from mysql
        mysqlop.execute("select keyword from key_words")
        keywords = mysqlop.fetchmany(size=10000000)

        # get site template from mysql
        mysqlop.execute("select id, cn_name, url, template, page_type, type from t_source_used where type='news' and cn_name='百度类别新闻'")
        ses = mysqlop.fetchmany(size=10000000)

        for item in keywords:
            key_word = item[0]
            for se in ses:
                type_page = se[4]
                source_name = se[1]

                # source time and key word not in table, then put it latest time in one month before
                insert_sql = "insert into source_latest_time(latest_time, source_name, key_word) values(%s, %s, %s)"
                initialize_crawl_time = datetime.strptime(CRAWLER_TIME_SIGN, '%Y-%m-%d %H:%M:%S')
                if source_name not in self.latest_time.keys():
                    self.latest_time[source_name] = dict()
                    self.latest_time[source_name][key_word] = SIGN_TIME_STAMP
                    mysqlop.execute(insert_sql, (initialize_crawl_time, source_name, key_word))
                    mysql_conn.commit()
                elif key_word not in self.latest_time[source_name].keys():
                    self.latest_time[source_name][key_word] = SIGN_TIME_STAMP
                    mysqlop.execute(insert_sql, (initialize_crawl_time, source_name, key_word))
                    mysql_conn.commit()

                self.selector = json.loads(se[3])
                # 根据关键词与站点的名字与pages生成对应的不同的url
                pageUrls = searResultPages(key_word, se[2], 1, int(pages), type_page)

                # 不同页面的url存储到start_urls中,start_urls中的每个url都会调用parse函数执行
                for url in pageUrls:
                    print(url)
                    self.start_urls.append(
                        {'url': url, 'selector': self.selector, 'source_name': source_name, 'key_word': key_word,
                          'type': se[5]})
        random.shuffle(self.start_urls)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url['url'], meta={'selector': url['selector'], 'source_name': url['source_name'],
                                            'key_word': url['key_word'],  'type': url['type']})

    def parse(self, response):

        self.selector = response.meta['selector']
        source_name = response.meta['source_name']
        key_word = response.meta['key_word']
        source_type = response.meta['type']

        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        blocks = Selector(response).xpath(self.selector['block'])
        print 'blocks len', len(blocks)

        for block in blocks:
            link = block.xpath(self.selector['link']).extract()
            title = block.xpath(self.selector['title']).extract()
            source = block.xpath(self.selector['from']).extract()

            if not isinstance(self.selector['abstract'], list):
                abstract = block.xpath(self.selector['abstract']).extract()
            else:
                abstract = block.xpath(self.selector['abstract'][0]).extract()
                get_abstract = ''.join(abstract).strip()
                if len(get_abstract) < 3:
                    abstract = block.xpath(self.selector['abstract'][1]).extract()

            if self.selector.has_key('time'):
                try:
                    ctime = block.xpath(self.selector['time']).extract()[0]
                except Exception, e:
                    ctime = block.xpath(self.selector['time']).extract()

                name = ''.join(source).strip()
                if name:
                    name = name.split(" ")[0]
                if source_type == 'news':
                    ctime = int(ctime)
                else:
                    ctime = transtime(ctime)
            else:
                try:
                    # print 'has no time'
                    string = ''.join(source).replace("\xc2\xa0", " ").split(' ', 1)
                    if len(string) >= 2:
                        ctime = transtime(string[1].strip().encode('utf-8'))
                        name = string[0].strip()
                    else:
                        ctime = None
                        name = source_name
                except Exception, e:
                    logging.error('extract time error', e)
                    ctime = None
                    name = source_name

            if ctime == None:
                # publish time 解析为空则设置为当前时间的unix时间戳
                ctime = int(time.time())

            self.item['publish_time'] = ctime
            self.item['From'] = source_type  # 此处改为type对应论坛新闻博客
            self.item['source_name'] = source_name
            self.item['key_word'] = key_word
            self.item['catch_date'] = str(int(time.time()))
            self.item['site_name'] = name
            self.item['url'] = ''.join(link).strip()
            self.item['title'] = ''.join(title).strip()
            self.item['summary'] = ''.join(abstract).strip()
            self.item['site_url'] = response.url

            if self.item['url']:

                # 为该条item确定类别
                if "item_class" in response.meta.keys():
                    self.item['item_class'] = response.meta['item_class']
                else:
                    self.item['item_class'] = md5(self.item["url"])

                self.item_json = json.dumps(self.item)
                # item_queue.put(item_json)
                yield Request(self.item['url'], meta={'item': self.item_json}, callback=self.parse_body)

                # 获得该条信息同类的一页信息的链接
                item_class = md5(self.item["url"])
                same_class_link = block.xpath(self.selector["same_class_link"]).extract()

                if len(same_class_link) == 1:
                    print 'find the same class'
                    same_class_link = same_class_link[0]
                    same_class_link = "http://news.baidu.com" + same_class_link
                    yield Request(same_class_link, meta={'selector': self.selector, 'source_name': source_name,
                                                    'key_word': key_word, 'type': source_type, 'item_class': item_class})

    def parse_body(self, response):
        """
        url_md5 as key, html body as value then save to redis
        :param response:
        :return:
        """
        item = response.meta['item']
        item = json.loads(item)
        body = response.body
        # 对html_body编码类型进行判断，不是unicode的进行转换
        if not isinstance(body, unicode):
            code_type = chardet.detect(body)['encoding']
            if code_type == 'GB2312':
                code_type = 'gbk'
            html_body = body.decode(code_type).encode('utf-8')
        else:
            html_body = body.encode('utf-8')

        item['html_body'] = html_body
        url_content = json.dumps(item)
        # url_content = item
        # url_content = item + '@' + body
        if len(body) > 5:
            content_queue.put(url_content)
        else:
            logging.info(response.url)
