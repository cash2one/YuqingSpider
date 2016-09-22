# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wtq'
import sys
reload(sys)
sys.path.append('/home/wtq/develop/workspace/github/YuqingSpider')
sys.setdefaultencoding('utf-8')
import time
import redis
import json
import random
from scrapy import Request
from scrapy.spiders import Spider
from ..common.md5 import md5
from ..common.searchEngines import news_site
from ..common.conn_mysql import conn_mysql
from ..common.searResultPages import searResultPages
from ..common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import Selector
from ..items.BaseItems import BaseItem
from ..util.transtime import transtime
from ..common.searchEngines import TurnPageByCount
from analyse_model.util.redis_queue import RedisQueue

item_queue = RedisQueue('newsitem')  # 'newsItem':[Item, Item, Item, Item]
content_queue = RedisQueue('newscontent')   # 'newsContent':[{url:}]
r = redis.StrictRedis(host='localhost', port=6379, db=0)
mysql_conn = conn_mysql()


class newsSpider(Spider):
    name = 'newsSpider'
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None
    item_json = None
    def __init__(self, keyword='石油', se='baidu', pages=1, *args, **kwargs):

        super(newsSpider, self).__init__(*args, **kwargs)
        # self.item = BaseItem()
        self.item = {}
        mysqlop = mysql_conn.cursor()
        # get key words from mysql
        mysqlop.execute("select keyword from key_words")
        keywords = mysqlop.fetchmany(size=100)
        # get site template from mysql
        mysqlop.execute("select en_name, ch_name, url, template from source_site where type='news'")
        ses = mysqlop.fetchmany(size=100)

        for item in keywords:
            # for se in ses:
            for se in ses:
                keyword = item[0]
                if se[0] in TurnPageByCount:
                    type_page = 1
                else:
                    type_page = 0

                spider_name = se[1]
                self.selector = json.loads(se[3])
                # self.selector = SearchEngineResultSelectors[self.searchEngine]
                # 根据关键词与站点的名字与pages生成对应的不同的url
                pageUrls = searResultPages(keyword, se[2], int(pages), type_page)

                # 不同页面的url存储到start_urls中,start_urls中的每个url都会调用parse函数执行
                for url in pageUrls:
                    print(url)
                    self.start_urls.append({'url': url, 'selector': self.selector, 'spider_name': spider_name})
        random.shuffle(self.start_urls)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url['url'], meta={'selector': url['selector'], 'spider_name': url['spider_name']})

    def parse(self, response):

        self.selector = response.meta['selector']
        spider_name = response.meta['spider_name']
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        blocks = Selector(response).xpath(self.selector['block'])

        for block in blocks:
            link = block.xpath(self.selector['link']).extract()
            title = block.xpath(self.selector['title']).extract()
            source = block.xpath(self.selector['from']).extract()
            abstract = block.xpath(self.selector['abstract']).extract()

            if self.selector.has_key('time'):
                ctime = block.xpath(self.selector['time']).extract()[0]
                name = ''.join(source).strip()
            else:
                try:
                    # print 'has no time'
                    string = ''.join(source).replace("\xc2\xa0", " ").split(' ', 1)
                    if len(string) >= 2:
                        ctime = transtime(string[1].strip())
                        name = string[0].strip()
                    else:
                        ctime = None
                        name = None
                except Exception, e:
                    print 'extract time error', e
                    # print ''.join(source), ''.join(title), 'error'

            self.item['publish_time'] = str(ctime)
            self.item['From'] = "1"  # 此处改为type对应论坛新闻博客
            self.item['spider_name'] = spider_name
            self.item['catch_date'] = str(int(time.time()))
            self.item['site_name'] = name
            self.item['url'] = ''.join(link).strip()
            self.item['title'] = ''.join(title).strip()
            self.item['summary'] = ''.join(abstract).strip()
            self.item['site_url'] = response.url
            if self.item['url']:
                # yield self.item
                self.item_json = json.dumps(self.item)
                # item_queue.put(item_json)
                yield Request(self.item['url'], meta={'item': self.item_json}, callback=self.parse_body)

    def parse_body(self, response):
        """
        url_md5 as key, html body as value then save to redis
        :param response:
        :return:
        """
        item = response.meta['item']
        body = response.body
        url_content = item + '@' + body

        if len(body) > 5:
            content_queue.put(url_content)

