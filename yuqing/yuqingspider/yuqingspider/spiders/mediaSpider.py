# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'tanlong'

import time
import json
import logging
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


class mediaSpider(Spider):
    """
    媒体的模板字段里多了 time_location字段 为0时 time在前，site_name在后.为1时，site_name在前,time在后
    """
    name = 'mediaSpider'
    start_urls = []
    searchEngine = None
    selector = None
    item_json = {}

    def __init__(self, pages=2, *args, **kwargs):
        super(mediaSpider, self).__init__(*args, **kwargs)

        mysqlop = mysql_conn.cursor()
        mysqlop.execute("SET NAMES utf8")
        mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
        mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
        mysql_conn.commit()

        mysqlop.execute("select keyword from key_words")
        keywords = mysqlop.fetchmany(size=10000000)

        # get site template from mysql
        mysqlop.execute(
            "select id, cn_name, url, template, page_type, type from t_source_used where type='media'")
        ses = mysqlop.fetchmany(size=10000000)

        # 构建url时默认keyword在前，page在后。当selector中有reverse字段时，转换page在前，keyword在后
        for item in keywords:
            key_word = item[0]
            for se in ses:
                source_name = se[1]
                selector = json.loads(se[3])
                type_page = se[4]

                if 'reverse' not in selector:
                    pageUrls = searResultPages(key_word, se[2], 1, int(pages), type_page)
                else:
                    pageUrls = searResultPages(key_word, se[2], 1, int(pages), type_page, 0)

                for url in pageUrls:
                    self.start_urls.append({'url': url, 'source_name': source_name, 'selector': selector, 'key_word': key_word})

    def start_requests(self):
        for url in self.start_urls:
            print "@@@@url@@@@@", url
            yield Request(url['url'], meta={'source_name': url['source_name'], 'selector': url['selector'],
                                            'key_word': url['key_word']})

    def parse(self, response):
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        key_word = response.meta['key_word']
        source_name = response.meta['source_name']
        self.selector = response.meta['selector']
        item = {}
        print "block first", self.selector["block"]

        blocks = Selector(response).xpath(self.selector['block'])

        for block in blocks:
            print "in block"

            link = block.xpath(self.selector['link']).extract()

            # title与abstract中会包含<font color ...>ff</font>这样重点加深的关键字，这样的提取xpath用list保存做特殊处理
            if not isinstance(self.selector['title'], list):
                title = block.xpath(self.selector['title']).extract()
            else:
                title_raw = block.xpath(self.selector['title'][0])
                title = title_raw.xpath("string(.)").extract()[0]

            if not isinstance(self.selector['abstract'], list):
                abstract = block.xpath(self.selector['abstract']).extract()
            else:
                abstract_raw = block.xpath(self.selector['abstract'][0])
                abstract = abstract_raw.xpath("string(.)").extract()[0]

            # 这种情况对应time与具体来源都在from字段获取
            if "from" in self.selector:
                source = block.xpath(self.selector['from']).extract()
                try:
                    # print 'has no time'
                    string = ''.join(source).replace("\xc2\xa0", " ").split(' ', 1)

                    if len(string) >= 2:
                        if self.selector['time_location']:

                            ctime = transtime(string[1].strip().encode('utf-8'))
                            name = string[0].strip()

                        else:
                            ctime = transtime(string[0].strip().encode("utf-8"))
                            name = string[1].strip()

                    else:
                        ctime = None
                        name = source_name

                    # 规范处理来源名
                    if source_name == "新华网":
                        name = str(name).split(" ")[-1]
                    elif source_name == "中新网":
                        name = str(name).split(" ")[0]

                except Exception, e:
                    logging.error('extract time error', e)
                    ctime = None
                    name = source_name

            # 这种情况对应只有time没有具体来源的
            if "time" in self.selector:
                ctime = block.xpath(self.selector['time']).extract()
                ctime = ctime[0]
                print "@@@@@@@ctime@@@@@@", ctime
                if source_name == "中青网" or source_name == "光明网" or source_name == "环球网":
                    ctime = str(ctime).split(" ")[-1]
                elif source_name == "央视网":
                    ctime = str(ctime.split("：")[-1])

                if source_name != "中新网":
                    # 非时间戳转化为时间戳
                    ctime = transtime(ctime)
                name = source_name

            item['publish_time'] = str(ctime)
            item['From'] = "media"
            item['catch_date'] = str(int(time.time()))
            # item['site_name'] = ''.join(source).strip().split(' - ')[0]
            item["site_name"] = name
            item['url'] = ''.join(link).strip()
            item['title'] = ''.join(title).strip()
            item['summary'] = ''.join(abstract).strip()
            item['site_url'] = response.url
            item['source_name'] = source_name
            item['key_word'] = key_word

            # print 'item url ', item
            print 'one item', item

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


