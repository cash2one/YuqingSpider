# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'tanlong'

import time
import json
import chardet
from scrapy import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider
from ..common.searResultPages import searResultPages
from ..common.conn_mysql import conn_mysql
from ..util.transtime import transtime
from ..util.redis_queue import RedisQueue

content_queue = RedisQueue('items')
mysql_conn = conn_mysql()


class blogSpider(Spider):

    name = 'blogSpider'
    start_urls = []
    searchEngine = None
    selector = None
    item_json = {}

    def __init__(self, pages=10, *args, **kwargs):
        super(blogSpider, self).__init__(*args, **kwargs)

        mysqlop = mysql_conn.cursor()
        mysqlop.execute("SET NAMES utf8")
        mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
        mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
        mysql_conn.commit()

        mysqlop.execute("select keyword from key_words")
        keywords = mysqlop.fetchmany(size=10000000)

        # get site template from mysql
        mysqlop.execute(
            "select id, cn_name, url, template, page_type, type from t_source_used where type='blog'")
        ses = mysqlop.fetchmany(size=10000000)

        for item in keywords:
            key_word = item[0]
            for se in ses:
                source_name = se[1]
                selector = json.loads(se[3])
                type_page = se[4]
                pageUrls = searResultPages(key_word, se[2], 1, int(pages), type_page)
                for url in pageUrls:
                    self.start_urls.append({'url': url, 'source_name': source_name, 'selector': selector, 'key_word': key_word})

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url['url'], meta={'source_name': url['source_name'], 'selector': url['selector'],
                                            'key_word': url['key_word']})

    def parse(self, response):
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        key_word = response.meta['key_word']
        source_name = response.meta['source_name']
        self.selector = response.meta['selector']
        item = {}
        blocks = Selector(response).xpath(self.selector['block'])
        for block in blocks:
            link = block.xpath(self.selector['link']).extract()
            title = block.xpath(self.selector['title']).extract()
            source = block.xpath(self.selector['from']).extract()
            _time = block.xpath(self.selector['time']).extract()
            abstract = block.xpath(self.selector['abstract']).extract()

            if self.selector.has_key('time'):
                if len(_time) >= 1:
                    ctime = transtime(_time[0])
                else:
                    ctime = int(time.time())

            item['publish_time'] = str(ctime)
            item['From'] = "blog"
            item['catch_date'] = str(int(time.time()))
            item['site_name'] = ''.join(source).strip().split(' - ')[0]
            item['url'] = ''.join(link).strip()
            item['title'] = ''.join(title).strip()
            item['summary'] = ''.join(abstract).strip()
            item['site_url'] = response.url
            item['source_name'] = source_name
            item['key_word'] = key_word

            if item['url']:
                item_json = json.dumps(item)
                yield Request(item['url'], meta={'item': item_json}, callback=self.parse_body)

    def parse_body(self, response):
        item = response.meta['item']
        body = response.body
        item = json.loads(item)

        if not isinstance(body, unicode):
            code_type = chardet.detect(body)['encoding']
            if code_type == 'GB2312':
                code_type = 'gbk'
            html_body = body.decode(code_type).encode('utf-8')
        else:
            html_body = body.encode('utf-8')

        item["html_body"] = html_body
        url_content = json.dumps(item)
        # print 'body', body
        if len(body) > 5:
            content_queue.put(url_content)


