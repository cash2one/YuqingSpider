# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'tanlong'

import time
import redis
from scrapy import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider
from ..common.searResultPages import searResultPages
from ..common.searchEngines import SearchEngineResultSelectors
from ..common.md5 import md5
from ..items.BaseItems import BaseItem
from ..util.transtime import transtime


r = redis.StrictRedis()


class blogSpider(Spider):
    name = 'blogSpider'
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None

    def __init__(self, keyword='游戏', se='sogoublog', pages = 30,  *args, **kwargs):
        super(blogSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword.lower()
        keywords = r.lrange('new_keyword', 0, 6)

        # for keyword in keywords:
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors[self.searchEngine]
        pageUrls = searResultPages(keyword, se, int(pages))
        for url in pageUrls:
            print(url)
            self.start_urls.append(url)

    def parse(self, response):
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        print self.selector
        item = BaseItem()
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
                    ctime = None

            item['publish_time'] = str(ctime)
            item['From'] = "3"
            item['spider_name'] = "blogSpider"
            item['catch_date'] = str(int(time.time()))
            item['site_name'] = ''.join(source).strip().split(' - ')[0]
            item['url'] = ''.join(link).strip()
            item['title'] = ''.join(title).strip()
            item['summary'] = ''.join(abstract).strip()
            item['site_url'] = response.url
            if item['url']:
                yield item
                # yield Request(item['url'], callback=self.parse_body)

    def parse_body(self, response):
        url_md5 = md5(response.url)
        r.set(url_md5, response.body)
